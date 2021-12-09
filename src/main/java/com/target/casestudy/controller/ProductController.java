package com.target.casestudy.controller;

import com.target.casestudy.entity.ProductInfo;
import com.target.casestudy.entity.CustomResponse;
import com.target.casestudy.service.ProductService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;


@RequestMapping(value="/products")
@RestController
@Slf4j
public class ProductController {

	@Autowired
	ProductService productService;


	@RequestMapping(value = "",method = RequestMethod.GET)
	public String getAll()
	{
		return "Hello world !";
	}


	@RequestMapping(value = "/{id}", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
	public HttpEntity<? extends Object> getProductInfo(@PathVariable("id") String productId) throws Exception {
		log.info("Inside getproductInfo  " + productId);
		CustomResponse response = new CustomResponse();
		ProductInfo product = null;
		try {
			product = productService.getProductDetails(productId);
		} catch (Exception e) {
			log.debug("Product Not Found Exception  " + e);
			throw new ResponseStatusException(
					HttpStatus.NOT_FOUND, "Product Not Found");
		}
		return new ResponseEntity<ProductInfo>(product, HttpStatus.OK);
	}

	@RequestMapping(value = "/{id}", method = RequestMethod.PUT, produces = "application/json")
	public ResponseEntity<CustomResponse> updatePrice(@RequestBody ProductInfo product,
													  @PathVariable("id") String productId) {
		CustomResponse response = new CustomResponse();
		try {
			if(product != null) {
				if(product.getId() != null && !product.getId().isEmpty())
				{
					if(product.getCurrent_price() != null)
					{
						productService.updateProductPrice(product);
						response.setMessage("Product updated successfully");
					}else
						response.setMessage("Please provide price info");
				}
				else
					response.setMessage("Please provide product id");
			}else
				response.setMessage("Product Info not available");
		} catch (Exception e) {
			log.debug("Product Not Found Exception while update " + e);
			throw new ResponseStatusException(
					HttpStatus.NOT_FOUND, "Product Not Found");
		}

		return new ResponseEntity<CustomResponse>(response,HttpStatus.OK);
	}
}
