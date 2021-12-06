## Business Problem 

<b>myRetail</b> is a rapidly growing company with HQ in Richmond, VA and over 200 stores across the east coast. myRetail wants to make its internal data available to any number of client devices, from myRetail.com to native mobile apps.
The goal for this exercise is to create an end-to-end Proof-of-Concept for a products API, which will aggregate product data from multiple sources and return it as JSON to the caller.
Your goal is to create a RESTful service that can retrieve product and price details by ID. The URL structure is up to you to define, but try to follow some sort of logical convention.
Build an application that performs the following actions:</br></br>
•	Responds to an HTTP GET request at /products/{id} and delivers product data as JSON (where {id} will be a number.
Example product IDs: 13860428, 54456119, 13264003, 12954218)

•	Example response: {"id":13860428,"name":"The Big Lebowski (Blu-ray) (Widescreen)","current_price":{"value": 13.49,"currency_code":"USD"}}

•	Performs an HTTP GET to retrieve the product name from an external API. (For this exercise the data will come from redsky.target.com, but let’s just pretend this is an internal resource hosted by myRetail)  

•	Example:
https://redsky-uat.perf.target.com/redsky_aggregations/v1/redsky/case_study_v1?key=3yUxt7WltYG7MFKPp7uyELi1K40ad2ys&tcin=13860428

•	Reads pricing information from a NoSQL data store and combines it with the product id and name from the HTTP request into a single response.

•	BONUS: Accepts an HTTP PUT request at the same path (/products/{id}), containing a JSON request body like the GET response, and updates the product’s price in the data store.  

*********************************************************************************************************************************
# __Solution:__

## __MyRetail API Solution provides the ability to:__

<ol>
  <li>Retrieve product and price information by Product Id.</li>
  <li>Update the price information in the database.</li>
  <li>Secure API with basic authentication.</li>
  <li>One rest end point is not recure.</li>	
  <li>Implement Swagger2 for API documentation</li>
</ol>
All the end points are totally secure in this application. I have implemented basic security and method level security as well. Update resource can be accessed by admin/admin user only.

                                   Method               Request                   Credentials
                                     GET              /products/{id}              [SECURE -- normaluser/normaluser]
                                     PUT              /products/{id}              [SECURE -- admin/admin]
					 GET              /products                   [NOT SECURE]

###### __Technology Stack:__

1. Spring Boot :
   https://start.spring.io/
   https://spring.io/guides/gs/serving-web-content/
2. Feign:
   Declarative REST Client: Feign creates a dynamic implementation of an interface decorated with JAX-RS or Spring MVC annotations.
   https://cloud.spring.io/spring-cloud-netflix/
3. MongoDB:
   https://www.mongodb.com/what-is-mongodb

4. Maven:
   https://maven.apache.org/
5. Mokito/Junit:
   http://site.mockito.org/
6. Postman:
   https://chrome.google.com/webstore/detail/postman/fhbjgbiflinjbdggehcddcbncdddomop?hl=en

###### __Setup instructions:__

1. Java 1.7
2. Eclipse  Mars: http://www.eclipse.org/downloads/packages/eclipse-ide-java-ee-developers/mars2
3. Install Mongo DB: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/
4. Install Maven: https://www.mkyong.com/maven/how-to-install-maven-in-windows/
5. Github:
   Download project from the following git repository
   https://github.com/rohitdec01/myRetail

a) Download as a ZIP file   OR

b) Clone the git project from git-bash or command prompt (You must have git setup)

6. Import the project into eclipse –   File->import


###### __Test the project:__

Test cases are present on the following directory. I have written some test cases for controller class and service  class using mokito. I am using mokito for mockdata.

C:\WORK_ENV\workspace\myRetail\src\test\java

To run the test  Go to project folder and trigger following command on the command prompt ( or gitbash).

mvn test.

###### __To run the application:__

Run mongo DB from the command prompt.  And test  ---  http://localhost:27017/  (default port)
Go to the project folder and trigger the command:

mvn spring-boot:run

###### __Check the http Request:__

### Secure API
The end point of this application is fully secure. There are 3 users in this application.
1. admin/admin   --- Can update price information and get the product by prodctId.
2. normaluser/normaluser  --  get the product by prodctId.
3. dbuser/dbuser  -- get the product by prodctId.
