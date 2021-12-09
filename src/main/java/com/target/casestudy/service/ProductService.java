package com.target.casestudy.service;

import java.io.IOException;
import java.util.List;
import java.util.Map;
import java.util.Objects;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.target.casestudy.entity.Product;
import com.target.casestudy.entity.ProductInfo;
import com.target.casestudy.repository.ProductRepository;
import com.target.casestudy.repository.ProductRepositoryImpl;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

import com.fasterxml.jackson.core.JsonParseException;
import com.fasterxml.jackson.databind.JsonMappingException;
import org.springframework.web.client.RestTemplate;

@Service
public class ProductService {
	protected Logger logger = LoggerFactory.getLogger(this.getClass());

	@Autowired
	private ProductRepository productRepository;

	@Autowired
	private RestTemplate restTemplate;

	@Value("${service.url}")
	private String baseUrl;

	@Autowired
	private ProductRepositoryImpl productRepositoryImpl;

	public ProductInfo getProductDetails(String productId) throws Exception
	{
		ProductInfo productResponse = null;
		try
		{
			// Get the product name from external API
			String name = this.getTitleForProduct(productId);

			// Get pricing info
			Product product = productRepository.getProductByproductId(productId);

			if(!Objects.isNull(product))
			{
				productResponse = new ProductInfo();
				productResponse.setId(productId);
				productResponse.setName(name);
				productResponse.setCurrent_price(product.getCurrent_price());
			}
		}catch (Exception ex)
		{
			throw  ex;
		}
		return productResponse;
	}

	private String getTitleForProduct(String productId) throws Exception {
		String title = "" ;

		Map<String, Map> infoMap = getProductInfoFromProductInfoService(productId);

		if(infoMap.size() > 0)
		{
			Map<String,Map> productMap = infoMap.get("data");
			if(productMap != null)
			{
				Map<String,Map> product = productMap.get("product");
				if(product != null)
				{
					Map<String,Map> itemMap = product.get("item");
					if (itemMap != null)
					{
						Map<String,String> productDescMap = itemMap.get("product_description");
						if(productDescMap != null)
							title = productDescMap.get("title");
					}
				}
			}
		}
        return title;
	}

	private Map<String, Map> getProductInfoFromProductInfoService(String productId) throws JsonParseException, JsonMappingException, IOException {
		Map<String, Map> result ;
		String url = baseUrl+productId;
		ResponseEntity<String> response
				= this.restTemplate.getForEntity(url, String.class);
		ObjectMapper mapper = new ObjectMapper();
		result = mapper.readValue(response.getBody(), Map.class);

		return result;
	}

	public void updateProductPrice(ProductInfo productInfo) throws Exception {
		// check if product exists
		Product product = this.productRepository.getProductByproductId(productInfo.getId());

		if(product != null)
		{
			Product newProduct = new Product();
			newProduct.setProductId(productInfo.getId());
			newProduct.setCurrent_price(productInfo.getCurrent_price());
			this.productRepositoryImpl.updatePriceInfo(productInfo.getCurrent_price(),productInfo.getId());
		}else
		{
			throw new Exception();
		}
	}
}
