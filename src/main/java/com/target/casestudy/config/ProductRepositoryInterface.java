package com.target.casestudy.config;

import java.util.Map;

public interface ProductRepositoryInterface {
    void updatePriceInfo(Map<String,String> priceInfo,String id);
}
