package com.example.portfolio.api.chatbot.service;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;

import java.util.HashMap;
import java.util.Map;
@Service
public class ChatbotService {

    @Value("${chatbot.api.url}")
    private String chatbotApiUrl;

    private final RestTemplate restTemplate;

    public ChatbotService() {
        this.restTemplate = new RestTemplate();
    }

    public String processMessage(String message) {
        try {
            // Flask API 호출을 위한 헤더 설정
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            // 요청 본문 생성
            Map<String, String> requestBody = new HashMap<>();
            requestBody.put("message", message);

            HttpEntity<Map<String, String>> request = new HttpEntity<>(requestBody, headers);

            // Flask API 호출
            ResponseEntity<ChatApiResponse> response = restTemplate.postForEntity(
                chatbotApiUrl + "/chat", 
                request, 
                ChatApiResponse.class
            );

            if (response.getBody() != null && "success".equals(response.getBody().getStatus())) {
                return response.getBody().getResponse();
            } else {
                return "죄송합니다. 응답을 처리하는 중에 오류가 발생했습니다.";
            }

        } catch (Exception e) {
            // 로깅 (실제 환경에서는 로거 사용)
            System.err.println("Chatbot API 호출 오류: " + e.getMessage());
            return "죄송합니다. 일시적인 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.";
        }
    }

    // Flask API 응답을 위한 DTO
    public static class ChatApiResponse {
        private String response;
        private String status;

        public String getResponse() { return response; }
        public void setResponse(String response) { this.response = response; }
        
        public String getStatus() { return status; }
        public void setStatus(String status) { this.status = status; }
    }
}