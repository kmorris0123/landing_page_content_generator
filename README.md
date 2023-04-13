Landing Page Content Generator

This script generates content for landing pages using OpenAI's GPT-3.5-turbo model. The generated content includes page titles, section headings, and the body text for each section. Users can choose to input a single keyword or import multiple keywords from a CSV file. The script allows users to manually enter section headings, use default headings, or generate them using ChatGPT.

Installation
Before running this script, you'll need to install the openai library. You can do this by running:

bash

pip install openai

Usage
Run the script:
bash

python landing_page_content_generator.py
Follow the prompts to provide the necessary information, such as company name, city, state, and keyword. You can either enter a single keyword or use a CSV file with multiple keywords.

Choose whether to manually enter section headings, use default headings, or generate them using ChatGPT.

Provide any additional notes or a company website link, if necessary.

Wait for the script to generate the content for each landing page. The content will be saved as text files in a folder named "{company_name} Landing Page Content".

Functions
create_page_title(keyword, city, state): Creates the page title using the provided keyword, city, and state.

replace_placeholders(section_title, keyword, city, state): Replaces placeholders in the section titles with the provided values.

generate_outline(page_title, company_name, keyword, city, state, num_sections, same_titles_for_all=False): Generates the section headings using ChatGPT or user input.

create_page_content(page_title, page_data, outline, company_name, keyword, city, state, notes, company_website): Generates the content for each section using ChatGPT and the provided information.

main(): Main function that handles user input, generates the content, and saves it to text files.

Example
The script will generate content for landing pages with titles, section headings, and body text. The output will be saved as text files in a folder named "{company_name} Landing Page Content". For example, if the company name is "Acme Corp", the folder will be named "Acme Corp Landing Page Content".

Note
This script uses OpenAI's GPT-3.5-turbo model, which requires an API key. Make sure to add your API key to the script:

openai.api_key = "your_openai_api_key_here"

Customization
This script allows for several levels of customization, from using default section headings to generating unique headings with ChatGPT. Users can also provide additional notes to guide the AI in generating more accurate and tailored content. To further customize the script, consider the following modifications:

Add more default section headings: Expand the list of default section headings to cover a wider range of topics. You can add them to the section_titles list when user_input == '2'.

Adjust the GPT-3.5-turbo parameters: Modify the parameters for the GPT-3.5-turbo model in the openai.ChatCompletion.create() function calls to change the behavior of the AI. For example, adjust the temperature parameter to control the randomness of the output.

Customize output format: Change the output format of the text files or save the output in a different file format, such as Markdown or HTML.

Add more prompts: Introduce additional prompts to guide the AI in generating content that better aligns with specific needs or requirements.

Limitations
The script's knowledge cutoff is September 2021; it may not have information on more recent events or developments.

Although the script generates coherent and engaging content, it may not always be factually accurate. It is recommended to verify the generated content for accuracy and make necessary edits.

The script is designed to generate content for landing pages; it may not perform as well when generating content for other purposes without further customization.

Contributing
Contributions to improve and expand the script are welcome. To contribute, please submit a pull request with your proposed changes.


License
This project is released under the MIT License.
