package com.example.portfolio.api.common.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class HomeController {

  @GetMapping("/")
  public String index() {
    return "index";
  }

  @GetMapping("/index")
  public String indexpage() {
    return "index";
  }

  @GetMapping("/about")
  public String about() {
    return "about";
  }

  @GetMapping("/resume")
  public String resume() {
    return "resume";
  }

  @GetMapping("/services")
  public String services() {
    return "services";
  }

  @GetMapping("/portfolio")
  public String portfolio() {
    return "portfolio";
  }

  @GetMapping("/contact")
  public String contact() {
    return "contact";
  }
}
