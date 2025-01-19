package mk.ukim.finki.wp.homework2das.web.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;
import org.springframework.http.ResponseEntity;

@RestController
public class SentimentController {

    @Autowired
    private RestTemplate restTemplate;

    @GetMapping("/get-sentiment")
    public String getSentiment(@RequestParam String tickerCode, @RequestParam String companyName) {
        String url = "http://localhost:5000/get-sentiment?ticker_code=" + tickerCode + "&company_name=" + companyName;

        // Call the Python API and get the response
        ResponseEntity<String> response = restTemplate.getForEntity(url, String.class);
        return response.getBody();
    }
}
