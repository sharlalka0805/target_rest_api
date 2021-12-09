package com.target.casestudy.service;

import static org.junit.Assert.assertEquals;

import java.util.HashMap;
import java.util.Map;

import com.target.casestudy.entity.Product;
import com.target.casestudy.entity.ProductInfo;
import com.target.casestudy.repository.ProductRepository;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.MockitoAnnotations;
import org.springframework.test.context.junit4.SpringRunner;

/**
 * @author Rohit Created On : 10/02/2017
 */
/**
 * @author Rohit
 *
 */
/**
 * @author Rohit
 *
 */
@RunWith(SpringRunner.class)
public class ProductServiceTest {

	@InjectMocks
	ProductService productService;

	@Mock // -- Spring Boot
	ProductRepository productrepositoryMock;



	/**
	 * Setup for Mockito before any test run.
	 */
	@Before
	public void setUp() {
		MockitoAnnotations.initMocks(this);
	}


	@Test
	public void getProductByIdTest() throws Exception {
		// Repository data from mock
		Map<String, String> currency = new HashMap<>();
		currency.put("value", "50");
		currency.put("currency_code", "USD");
		Product mockProduct = new Product("13860428", currency);
		System.out.println(productrepositoryMock);
		Mockito.when(productrepositoryMock.getProductByproductId(Mockito.anyString())).thenReturn(mockProduct);

		//Mockito.when(productInfoClient.getProductInfoById(Mockito.anyString()))
		//		.thenReturn(new ProductInfoClientMock().getProductInfoById("13860428"));

		// Actual Result
		ProductInfo actualProduct = productService.getProductDetails("13860428");

		// Expected Result
		Map<String, String> currency1 = new HashMap<>();
		currency.put("value", "50");
		currency.put("currency_code", "USD");
		Product expectedProduct = new Product("13860428", currency1);

		assertEquals(expectedProduct.getProductId(), actualProduct.getId());
	}


	@Test(expected = NullPointerException.class)
	public void getProductInfoTest_wrongProductId() throws Exception {

		Map<String, String> currency = new HashMap<>();
		currency.put("value", "50");
		currency.put("currency_code", "USD");
		Product mockProduct = new Product("13860428",  currency);
		Mockito.when(productrepositoryMock.getProductByproductId(Mockito.anyString())).thenReturn(mockProduct);

		productService.getProductDetails("12345678");
	}
}
