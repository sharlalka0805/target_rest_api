package com.target.casestudy.service;

import java.io.IOException;
import java.util.Map;
import java.util.Objects;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.target.casestudy.entity.Product;
import com.target.casestudy.entity.ProductInfo;
import com.target.casestudy.repository.ProductRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
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
				productResponse.setProductId(productId);
				productResponse.setProductTitle(name);
				productResponse.setPrice(product.getCurrent_price());
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
		RestTemplate restTemplate = new RestTemplate();
		String url = "https://redsky-uat.perf.target.com/redsky_aggregations/v1/redsky/case_study_v1?key=3yUxt7WltYG7MFKPp7uyELi1K40ad2ys&tcin="+productId;
		ResponseEntity<String> response
				= restTemplate.getForEntity(url, String.class);
		ObjectMapper mapper = new ObjectMapper();
		result = mapper.readValue(response.getBody(), Map.class);

		return result;
	}

	public void updateProductPrice(ProductInfo productInfo) {
		// check if product exists
		Product product = productRepository.getProductByproductId(productInfo.getProductId());

		if(product != null)
		{
			Product newProduct = new Product();
			newProduct.setProductId(productInfo.getProductId());
			newProduct.setCurrent_price(productInfo.getPrice());
			productRepository.save(product);
		}
	}

}
