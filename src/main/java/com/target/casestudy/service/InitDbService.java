package com.target.casestudy.service;

import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.annotation.PostConstruct;

import com.target.casestudy.entity.Product;
import com.target.casestudy.repository.ProductRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;


@Service
public class InitDbService {

	@Autowired
	private ProductRepository productRepository;

	public InitDbService() {
		// TODO Auto-generated constructor stub
	}

	/**
	 * Populate data after initialize the application.
	 */
	@PostConstruct
	public void init() {
		addProduct();

	}

	/**
	 * Add dummy products.
	 */
	private void addProduct() {
		if (productRepository != null) {
			Map<String, String> currency1 = new HashMap<>();
			currency1.put("value", "50");
			currency1.put("currency_code", "USD");
			Product product1 = new Product("13860428", currency1);

			Map<String, String> currency2 = new HashMap<>();
			currency2.put("value", "100.50");
			currency2.put("currency_code", "USD");
			Product product2 = new Product("54456119",  currency2);

			Map<String, String> currency3 = new HashMap<>();
			currency3.put("value", "55");
			currency3.put("currency_code", "USD");
			Product product3 = new Product("13264003", currency3);

			Map<String, String> currency4 = new HashMap<>();
			currency4.put("value", "105.50");
			currency4.put("currency_code", "USD");
			Product product4 = new Product("12954218", currency4);

			// delete previous data
			this.productRepository.deleteAll();

			// Add product List in db.
			List<Product> products = Arrays.asList(product1, product2, product3, product4);
			this.productRepository.saveAll(products);
		}
	}

}
