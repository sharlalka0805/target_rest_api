package com.target.casestudy.entity;

import java.util.Map;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

@Document(collection="products")
public class Product {

	@Id
	public String productId;

	@Field("current_price")
	public Map<String, String> current_price;

	public Product() {
		// TODO Auto-generated constructor stub
	}

	public Product(String productId, Map<String, String> current_price) {
		this.productId = productId;
		this.current_price = current_price;
	}

	public String getProductId() {
		return productId;
	}

	public void setProductId(String productId) {
		this.productId = productId;
	}

	public Map<String, String> getCurrent_price() {
		return current_price;
	}

	public void setCurrent_price(Map<String, String> current_price) {
		this.current_price = current_price;
	}

}
