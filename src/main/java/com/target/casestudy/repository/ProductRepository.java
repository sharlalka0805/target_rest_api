package com.target.casestudy.repository;

import com.target.casestudy.entity.Product;
import org.springframework.data.mongodb.repository.MongoRepository;


public interface ProductRepository extends MongoRepository<Product, String> {
	
	/**
	 * @param productId
	 * @return
	 */
	public Product getProductByproductId(String productId);
}
