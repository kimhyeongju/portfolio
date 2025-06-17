package com.example.portfolio.api.chatbot.controller;

import com.example.portfolio.api.chatbot.service.ChatbotService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

@Controller
@RequiredArgsConstructor
public class ChatbotController {

    private final ChatbotService chatbotService;

    @GetMapping("/chatbot")
    public String chatbot() {
        return "chatbot";
    }

    @PostMapping("/api/chat")
    @ResponseBody
    public ResponseEntity<?> chat(@RequestBody ChatRequest request) {
        try {
            String response = chatbotService.processMessage(request.getMessage());
            return ResponseEntity.ok(new ChatResponse(response, "success"));
        } catch (Exception e) {
            return ResponseEntity.status(500)
                .body(new ChatResponse("죄송합니다. 일시적인 오류가 발생했습니다.", "error"));
        }
    }

    // DTO 클래스들
    public static class ChatRequest {
        private String message;
        
        public String getMessage() { return message; }
        public void setMessage(String message) { this.message = message; }
    }

    public static class ChatResponse {
        private String response;
        private String status;
        
        public ChatResponse(String response, String status) {
            this.response = response;
            this.status = status;
        }
        
        public String getResponse() { return response; }
        public String getStatus() { return status; }
    }
}
