package com.badsector.radiologyassistant.controller;

import com.badsector.radiologyassistant.service.FileStorageService;
import com.badsector.radiologyassistant.service.TranscriptionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;

import java.nio.file.Path;

@Controller
public class UploadController {

    private final FileStorageService fileStorageService;
    private final TranscriptionService transcriptionService;

    @Autowired
    public UploadController(FileStorageService fileStorageService, TranscriptionService transcriptionService) {
        this.fileStorageService = fileStorageService;
        this.transcriptionService = transcriptionService;
    }

    @PostMapping("/upload")
    public String handleUpload(@RequestParam("audioFile") MultipartFile audioFile, Model model) {
        try {
            Path storedPath = fileStorageService.store(audioFile);
            String transcript = transcriptionService.transcribe(storedPath);
            model.addAttribute("transkript", transcript);
        } catch (Exception e) {
            model.addAttribute("transkript", "Error processing file: " + e.getMessage());
        }
        return "index";
    }
}
