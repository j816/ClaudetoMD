# Claude Process GUI

This is a graphical user interface (GUI) application that processes text files using the Anthropic Claude API. It allows users to select a prompt file, multiple text files, and an output directory, and then processes the files using the Claude API to generate markdown output.

## Purpose

The Claude Process GUI simplifies the task of applying a single prompt to multiple text files. This can be useful in various scenarios, such as:

- Summarizing a collection of articles or documents
- Generating responses to a set of customer inquiries
- Analyzing sentiment across multiple reviews or feedback submissions
- Extracting key information from a series of reports

By using the Anthropic Claude API, the application leverages powerful language models to process and generate meaningful output from the input text files.

## Example Use Cases

1. **Article Summarization**: You have a collection of news articles or blog posts that you want to summarize. Create a prompt file with instructions like "Summarize the following article in 3-5 sentences: {{TEXT}}", select the articles as input text files, and let the application generate concise summaries for each article.

2. **Customer Support Responses**: You have a set of common customer inquiries or support tickets. Create a prompt file with a template response, such as "Thank you for contacting us. Regarding your issue: {{TEXT}}, here are some steps you can try: ...". Select the customer inquiries as input text files, and the application will generate personalized responses for each inquiry.

3. **Sentiment Analysis**: You have a dataset of product reviews or customer feedback. Create a prompt file with instructions like "Analyze the sentiment of the following review (positive, negative, or neutral) and provide a brief explanation: {{TEXT}}". Select the reviews as input text files, and the application will perform sentiment analysis on each review.

4. **Information Extraction**: You have a collection of reports or documents containing specific information you want to extract. Create a prompt file with instructions like "Extract the following information from the given text: date, location, key findings. {{TEXT}}". Select the reports as input text files, and the application will attempt to extract the requested information from each document.

## Getting Started

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set up your Anthropic API key in the application's settings tab.

3. Prepare your prompt file. The prompt file should include the `{{TEXT}}` placeholder, which will be replaced with the content of each input text file during processing.

4. Launch the application:
   ```
   python anmd.py
   ```

5. In the application's main tab:
   - Select your prompt file
   - Select one or more input text files
   - Choose an output directory where the generated markdown files will be saved

6. Click the "Process" button to start processing the files. The application will process each input text file using the specified prompt and generate corresponding markdown files in the output directory.

7. Monitor the progress and any logs in the application's log window.

## Configuration

- You can save and load configuration settings using the "Save Config" and "Load Config" buttons in the main tab. This allows you to quickly set up the application with previously used prompt files, input text files, and output directories.

- The application automatically saves your Anthropic API key and temperature settings for future use.

## Troubleshooting

- If you encounter any issues or errors, check the application's log window for details.
- Make sure you have a valid Anthropic API key set up in the settings tab.
- Ensure that your prompt file includes the `{{TEXT}}` placeholder.
- Verify that the input text files and output directory are accessible and have the necessary permissions.

If you have any further questions or need assistance, please refer to the documentation or contact the application's developer.
