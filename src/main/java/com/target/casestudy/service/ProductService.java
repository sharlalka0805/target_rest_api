package com.target.casestudy.service;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

import com.target.casestudy.entity.Product;
import com.target.casestudy.repository.ProductRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

import com.fasterxml.jackson.core.JsonParseException;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.web.client.RestTemplate;

@Service
public class ProductService {
    protected Logger logger = LoggerFactory.getLogger(this.getClass());

    @Autowired
    private RestTemplate restTemplate;

    @Autowired
    private ProductRepository productRepository;

    private final String PRODUCTS_PRODUCT_ID = "/products/{id}";

    public ProductService() {

    }

    /**
     * @param productId
     * @return
     * @throws JsonParseException
     * @throws JsonMappingException
     * @throws IOException
     */
    public Product getProductById(String productId) throws JsonParseException, JsonMappingException, IOException {
        // From application DB
        Product product = productRepository.getProductByproductId(productId);
        // From external API
        product.setTitle(this.getTitleForProduct(productId));
        logger.info("Title from RFemote API   "+ product.getTitle());
        return product;
    }

    /**
     * @param productId
     * @return
     * @throws IOException
     * @throws JsonMappingException
     * @throws JsonParseException
     * @throws Exception
     *
     * get the title from
     */
    @SuppressWarnings({"unchecked","rawtypes"})
    private String getTitleForProduct(String productId) throws JsonParseException, JsonMappingException, IOException {
        Map<String, Map> infoMap = getProductInfoFromProductInfoService(productId);

        Map<String,Map> productMap = infoMap.get("product");
        Map<String,Map> itemMap = productMap.get("item");
        Map<String,String> prodDescrMap = itemMap.get(("product_description"));

        return prodDescrMap.get("title");
    }

    /**
     * @param productId
     * @return
     * @throws JsonParseException
     * @throws JsonMappingException
     * @throws IOException
     *
     * Getting remote data using Feign product service.
     */
    @SuppressWarnings({"unchecked","rawtypes"})
    private Map<String, Map> getProductInfoFromProductInfoService(String productId) throws JsonParseException, JsonMappingException, IOException {
        ObjectMapper infoMapper = new ObjectMapper();
        Map<String, String> params = new HashMap<String, String>();
        params.put("tcin", productId);
        ResponseEntity<String> response = restTemplate
                .getForEntity(PRODUCTS_PRODUCT_ID, String.class, params);
        System.out.println(response.getStatusCode().value());
        Map<String, Map> infoMap = infoMapper.readValue(response.getBody(), Map.class);
        return infoMap;
    }

    /**
     * @param product
     */
    public void updateProductById(Product product) {
        productRepository.save(product);
    }

}
