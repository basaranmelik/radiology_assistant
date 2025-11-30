package com.badsector.radiologyassistant.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import jakarta.annotation.PostConstruct;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.util.UUID;

@Service
public class FileStorageService {

    @Value("${user.dir}")
    private String projectRoot;

    private Path audioDir;
    private Path outputDir;

    @PostConstruct
    public void init() throws IOException {
        // Base directory is the project root
        Path baseDir = Path.of(projectRoot);
        audioDir = baseDir.resolve("data/audio");
        outputDir = baseDir.resolve("data/output");
        Files.createDirectories(audioDir);
        Files.createDirectories(outputDir);
    }

    /**
     * Stores the uploaded multipart file in the audio directory with a random UUID
     * filename.
     * Returns the absolute path to the stored file.
     */
    public Path store(MultipartFile file) throws IOException {
        if (file.isEmpty()) {
            throw new IOException("Uploaded file is empty");
        }
        String originalFilename = file.getOriginalFilename();
        String extension = "";
        if (originalFilename != null && originalFilename.contains(".")) {
            extension = originalFilename.substring(originalFilename.lastIndexOf('.'));
        }
        String filename = UUID.randomUUID().toString() + extension;
        Path destination = audioDir.resolve(filename);
        Files.copy(file.getInputStream(), destination, StandardCopyOption.REPLACE_EXISTING);
        return destination.toAbsolutePath();
    }

    public Path getOutputDir() {
        return outputDir;
    }
}
