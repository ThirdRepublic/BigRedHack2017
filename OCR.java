
import java.net.URI;
import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.client.utils.URIBuilder;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;
import org.json.JSONML;
import org.json.JSONObject;

public class OCR
{
    // **********************************************
    // *** Update or verify the following values. ***
    // **********************************************
	
    // Replace the subscriptionKey string value with your valid subscription key.
    public static final String subscriptionKey = "da5cec920bae4fd68a089a7253fdd063";

    // Replace or verify the region.
    //
    // You must use the same region in your REST API call as you used to obtain your subscription keys.
    // For example, if you obtained your subscription keys from the westus region, replace
    // "westcentralus" in the URI below with "westus".
    //
    // NOTE: Free trial subscription keys are generated in the westcentralus region, so if you are using
    // a free trial subscription key, you should not need to change this region.
    //
    // Also, if you want to use the celebrities model, change "landmarks" to "celebrities" here and in
    // uriBuilder.setParameter to use the Celebrities model.
    public static final String uriBase = "https://eastus2.api.cognitive.microsoft.com/vision/v1.0/ocr";


    public static void main(String[] args)
    {
        HttpClient httpClient = new DefaultHttpClient();

        try
        {
            // NOTE: You must use the same location in your REST call as you used to obtain your subscription keys.
            //   For example, if you obtained your subscription keys from westus, replace "westcentralus" in the
            //   URL below with "westus".
            URIBuilder uriBuilder = new URIBuilder(uriBase);

            uriBuilder.setParameter("language", "unk");
            uriBuilder.setParameter("detectOrientation ", "true");

            // Request parameters.
            URI uri = uriBuilder.build();
            HttpPost request = new HttpPost(uri);

            // Request headers.
            request.setHeader("Content-Type", "application/json");
            request.setHeader("Ocp-Apim-Subscription-Key", subscriptionKey);

            // Request body.
            StringEntity requestEntity =
                    new StringEntity("{\"url\":\"https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Atomist_quote_from_Democritus.png/338px-Atomist_quote_from_Democritus.png\"}");
            request.setEntity(requestEntity);

            // Execute the REST API call and get the response entity.
            HttpResponse response = httpClient.execute(request);
            HttpEntity entity = response.getEntity();

            if (entity != null)
            {
                // Format and display the JSON response.
                String jsonString = EntityUtils.toString(entity);
                JSONObject json = new JSONObject(jsonString);
                System.out.println("REST Response:\n");
                System.out.println(json.toString(2));
                System.out.println(jsonString);
                System.out.println(json.getJSONArray("regions").getJSONObject(0).getJSONArray("lines").getJSONObject(0));
            }
        }
        catch (Exception e)
        {
            // Display error message.
            System.out.println(e.getMessage());
        }
    }
    
	/*
	public static void main(String[] args)
    {
		JSONObject test = new JSONObject();
		test.put("hello", new JSONObject().put("idk", "i forgot java lol"));
		System.out.println(test);*/
				/*Json.createObjectBuilder()
		     .add("firstName", "John")
		     .add("lastName", "Smith")
		     .add("age", 25)
		     .add("address", Json.createObjectBuilder()
		         .add("streetAddress", "21 2nd Street")
		         .add("city", "New York")
		         .add("state", "NY")
		         .add("postalCode", "10021"))
		     .add("phoneNumber", Json.createArrayBuilder()
		         .add(Json.createObjectBuilder()
		             .add("type", "home")
		             .add("number", "212 555-1234"))
		         .add(Json.createObjectBuilder()
		             .add("type", "fax")
		             .add("number", "646 555-4567")))
		     .build();*/
    //}
}