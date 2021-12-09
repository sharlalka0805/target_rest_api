package com.target.casestudy.controller;


import java.util.HashMap;
import java.util.Map;

import com.target.casestudy.entity.Product;
import com.target.casestudy.service.ProductService;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.MockitoAnnotations;
import org.skyscreamer.jsonassert.JSONAssert;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.test.web.servlet.RequestBuilder;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest(value = ProductController.class)
@RunWith(SpringRunner.class)
public class ProductControllerTest {
	protected Logger logger = LoggerFactory.getLogger(this.getClass());

	@Autowired
	MockMvc mockMvc;

	@MockBean
	ProductService productServiceMock;

	/**
	 * Setup for Mockito before any test run.
	 */
	@Before
	public void setUp() {
		MockitoAnnotations.initMocks(this);
	}

	@Test
	public void getProductInfoTest() throws Exception {
		// service data from mock
		Map<String, String> currency = new HashMap<>();
		currency.put("value", "50");
		currency.put("currency_code", "USD");
		Product mockProduct = new Product("13860428", currency);

		//Mockito.when(productServiceMock.getProductById(Mockito.anyString())).thenReturn(mockProduct);

		String url = "/products/13860428";
		RequestBuilder requestBuilder = MockMvcRequestBuilders.get(url).accept(MediaType.APPLICATION_JSON_VALUE);

		// Actual Result
		MvcResult result = mockMvc.perform(requestBuilder).andReturn();
		// Expected Result
		String expectedProductJson = "{\"productId\": \"13860428\",\"title\": \"The Big Lebowski (Blu-ray)\",\"current_price\": {\"value\": \"50\",\"currency_code\": \"USD\"}}";

		JSONAssert.assertEquals(expectedProductJson, result.getResponse().getContentAsString(), false);
	}


	@Test
	public void getProductInfoTest_wrongProductId() throws Exception {
		/*Mockito.when(productServiceMock.getProductById(Mockito.anyString())).thenThrow(new NullPointerException());

		try {
			String url = "/products/123456";
			RequestBuilder requestBuilder = MockMvcRequestBuilders.get(url).accept(MediaType.APPLICATION_JSON_VALUE);
			mockMvc.perform(requestBuilder).andReturn();
		} catch (ProductNotFoundException e) {
			logger.debug("Product not found Exception test sucess.");
		}*/
	}
}
