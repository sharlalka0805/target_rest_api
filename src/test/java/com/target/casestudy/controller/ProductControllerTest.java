package com.target.casestudy.controller;


import java.util.HashMap;
import java.util.Map;

import com.target.casestudy.entity.Product;
import com.target.casestudy.entity.ProductInfo;
import com.target.casestudy.service.ProductService;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mockito;
import org.mockito.MockitoAnnotations;
import org.skyscreamer.jsonassert.JSONAssert;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
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

	@Autowired
	ProductController controller;

	@Before
	public void setUp() {
		MockitoAnnotations.initMocks(this);
	}

	@Test
	public void getProductInfoTest() throws Exception {
		Map<String, String> currency = new HashMap<>();
		currency.put("value", "50");
		currency.put("currency_code", "USD");

		ProductInfo mockProduct = new ProductInfo();
		mockProduct.setId("13860428");
		mockProduct.setName("Test");
		mockProduct.setCurrent_price(currency);

		Mockito.when(productServiceMock.getProductDetails(Mockito.anyString())).thenReturn(mockProduct);

		ResponseEntity<ProductInfo> response = (ResponseEntity<ProductInfo>) controller.getProductInfo("13860428");

	}

}
