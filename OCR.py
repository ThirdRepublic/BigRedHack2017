########### Python 2.7 #############
import httplib, urllib, base64, json

# Word class needed to not die over all of the information gathering
class Word:
    def __init__(self, x, y, width, text):
        self.x = x
        self.y = y
        self.width = width
        self.text = text
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getWidth(self):
        return self.width
    def getText(self):
        return self.text

# words is an array of Word objects
def mergeSort(words):
    if len(words)>1:
        mid = len(words)//2
        lefthalf = words[:mid]
        righthalf = words[mid:]

        mergeSort(lefthalf)
        mergeSort(righthalf)

        i=0
        j=0
        k=0
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i].getY() < righthalf[j].getY() + 5  or (lefthalf[i].getY() == righthalf[j].getY() and lefthalf[i].getX() < righthalf[j].getY()):
                words[k]=lefthalf[i]
                i=i+1
            else:
                words[k]=righthalf[j]
                j=j+1
            k=k+1

        while i < len(lefthalf):
            words[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j < len(righthalf):
            words[k]=righthalf[j]
            j=j+1
            k=k+1

###############################################
#### Update or verify the following values. ###
###############################################

# Replace the subscription_key string value with your valid subscription key.
subscription_key = 'da5cec920bae4fd68a089a7253fdd063'

# Replace or verify the region.
#
# You must use the same region in your REST API call as you used to obtain your subscription keys.
# For example, if you obtained your subscription keys from the westus region, replace
# "westcentralus" in the URI below with "westus".
#
# NOTE: Free trial subscription keys are generated in the westcentralus region, so if you are using
# a free trial subscription key, you should not need to change this region.
uri_base = 'eastus2.api.cognitive.microsoft.com'

headers = {
    # Request headers.
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': subscription_key,
}

params = urllib.urlencode({
    # Request parameters. The language setting "unk" means automatically detect the language.
    'language': 'unk',
    'detectOrientation ': 'true',
})


def crack(url):

    # The URL of a JPEG image containing text.
    body = "{'url':'" + url + "'}"

    try:
        # Execute the REST API call and get the response.
        conn = httplib.HTTPSConnection('eastus2.api.cognitive.microsoft.com')
        conn.request("POST", "/vision/v1.0/ocr?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()

        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed = json.loads(data)

        #print(parsed)

        xCoords = []
        yCoords = []
        width = []
        words = []
        wordList = []

        page = []
        row = []
        page.append(row) # dummy row
        column = []
        #print ("Response:")
        for dictionary in parsed["regions"]:
            for sub in dictionary["lines"]:
                for item in sub["words"]:
                    for key in item:
                        if key == 'boundingBox':
                            xCoords.append(item[key].split(',')[0])
                            yCoords.append(item[key].split(',')[1])
                            width.append(item[key].split(',')[2])
                        else:
                            words.append(item[key])

        for i in range(len(words)):
            z = Word(int(xCoords[i]), int(yCoords[i]), int(width[i]), words[i])
            wordList.append(z)

        mergeSort(wordList)

        currWord = Word(0, 0, 0, '')
        prevWord = Word(0, 0, 0, '')
        for i in range(len(words)):
            currWord = wordList[i]

            if (currWord.getY() < prevWord.getY() + 5 and currWord.getY() > prevWord.getY() - 5):
                # print "passed y check"
                if (currWord.getX() < prevWord.getX() + prevWord.getWidth() + 20 and currWord.getX() > prevWord.getX() + prevWord.getWidth() - 20):
                    # print "passed x check"
                    column.append(currWord)
                else:
                    # print "failed x check"
                    row.append(column)
                    column = []
                    column.append(currWord)
            else:
                # print "failed y check"
                row.append(column)
                page.append(row)
                row = []
                column = []
                column.append(currWord)

            prevWord = currWord
            if (i == len(words) - 1):
                row.append(column)
                page.append(row)

        return_string = ""
        for rows in page:
            for columns in rows:
                for word in columns:
                    return_string += word.getText()
                return_string += "          "
            return_string += "\n"
        # print (json.dumps(parsed, sort_keys=True, indent=2))
        conn.close()

        return return_string

    except Exception as e:
        return "Error:", str(e)

####################################