Adobe Hackathon Round 1B – Offline Paper Analyzer

This project extracts key sections like "method", "dataset", and "benchmark "from offline PDF research papers and generates a structured summary.

How to Build and Run (Docker)

```bash
docker build --platform linux/amd64 -t offline-paper-analyzer .
docker run --rm -v "%cd%\input:/app/input" -v "%cd%\output:/app/output" --network none offline-paper-analyzer
