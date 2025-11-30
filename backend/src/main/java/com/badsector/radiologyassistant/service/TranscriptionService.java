package com.badsector.radiologyassistant.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

@Service
public class TranscriptionService {

    @Value("${user.dir}")
    private String projectRoot;

    /**
     * Invokes the Python orchestrator script with the given audio file path.
     * Returns the transcript string extracted from the script's standard output.
     */
    public String transcribe(Path audioFilePath) throws IOException, InterruptedException {
        // projectRoot is .../backend
        // orchestrator is in .../ai/src/orchestrator.py
        Path scriptPath = Path.of(projectRoot).getParent().resolve("ai/src/orchestrator.py");

        List<String> command = new ArrayList<>();
        command.add("python");
        command.add(scriptPath.toString());
        command.add("--audio_file");
        command.add(audioFilePath.toString());

        ProcessBuilder pb = new ProcessBuilder(command);
        pb.redirectErrorStream(true);
        Process process = pb.start();

        StringBuilder output = new StringBuilder();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()))) {
            String line;
            while ((line = reader.readLine()) != null) {
                output.append(line).append("\n");
            }
        }
        int exitCode = process.waitFor();
        if (exitCode != 0) {
            throw new IOException("Orchestrator exited with code " + exitCode + "\nOutput: " + output.toString());
        }
        // The orchestrator prints the full transcript early in the logs.
        // We'll extract the line that starts with "Tam Transkript Alındı." or the
        // following line.
        String[] lines = output.toString().split("\n");
        for (int i = 0; i < lines.length; i++) {
            if (lines[i].contains("Tam Transkript Alındı")) {
                // The transcript is printed just after this line in the original script.
                if (i + 1 < lines.length) {
                    return lines[i + 1].trim();
                }
            }
        }
        // Fallback: return full output.
        return output.toString().trim();
    }
}
