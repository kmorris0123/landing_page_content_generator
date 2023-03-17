import openai
import csv
import os

# Where you add the Openai key
openai.api_key = ""

# this creates the page titles
def create_page_title(keyword, city, state):
    return f"{keyword} in {city}, {state}"

# this function replaces place holder text
def replace_placeholders(section_title, keyword, city, state):
    placeholders = ["{keyword}", "{city}", "{state}"]
    values = [keyword, city, state]
    for placeholder, value in zip(placeholders, values):
        section_title = section_title.replace(placeholder, value)
    return section_title


def generate_outline(page_title, company_name, keyword, city, state, num_sections, same_titles_for_all=False):
    if same_titles_for_all:
        section_titles = []
        for i in range(num_sections):
            section_title = input(f"Enter section {i+1} title: ")
            section_titles.append(replace_placeholders(section_title, keyword, city, state))
    else:
        outline_prompt = [
            {"role": "system", "content": "You are an AI language model."},
            {"role": "user", "content": f"Write an outline with {num_sections} section headings for a landing page titled '{page_title}' for {company_name} that targets {keyword} in {city}, {state}. The landing page should focus on the unique benefits of {keyword} and should be tailored to appeal to their audience. Please provide creative and attention-grabbing section headings that are specific to the topic."}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=outline_prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
        )

        section_titles = response.choices[0].message['content'].strip().split("\n")[:num_sections]
        section_titles = [replace_placeholders(title, keyword, city, state) for title in section_titles]

    return section_titles

def create_page_content(page_title, page_data, outline, company_name, keyword, city, state, notes, company_website):
    content = ""
    summary = ""
    for section in outline:
        section_prompt = [
            {"role": "system", "content": "You are an AI language model."},
            {"role": "user", "content": f"Write a few paragraphs about {section} for {company_name} located in {city}, {state}. Use the provided summary to make sure the output flows well with the previous information: {summary}. To ensure a well-written output, please follow these guidelines: Avoid repeating any sentences or information from summary given to keep the content cohesive and unique. Use creative and attention-grabbing introductory sentences for each paragraph. Limit the mention of the company name to only once per output to avoid redundancy. Avoid beginning any paragraph with 'At {company_name},' to add variety and maintain a smooth flow. {notes} {company_website}."}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=section_prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
        )

        section_content = response.choices[0].message['content'].strip()
        content += f"{section}\n{section_content}\n\n"

        prompt = [
            {"role": "system", "content": "You are an AI language model."},
            {"role": "user", "content": f"Please summarize the previous section's content into a couple sentences. The content that needs to be summarized is as follows: {content}. Your summary should provide a concise overview of the previous section's key points, allowing readers to quickly grasp the content's main ideas. This will help keep the landing page focused and coherent, making it easier for readers to engage with         the content. Also, always say if the company name was mentioned"}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
        )

        summary = response.choices[0].message['content'].strip()

    return content.strip()



def main():

    # Ask the user if they want to enter a single keyword or use a CSV file
    data_source = input("Enter '1' for a single keyword or '2' to use a CSV file: ")

    if data_source == '1':
        # Get user input for company name, city, state, and keyword
        company_name = input("Enter company name: ")
        city = input("Enter city: ")
        state = input("Enter state: ")
        keyword = input("Enter keyword: ")

        # Create a dictionary for the single keyword entry
        page_data_dict = {
            create_page_title(keyword, city, state): {
                "keyword": keyword,
                "city": city,
                "state": state
            }
        }
    elif data_source == '2':
        # Read CSV and create dictionary
        csv_filename = input("Enter CSV filename: ")
        with open(csv_filename) as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # skip header row
            page_data_dict = {}

            # Create a dictionary for each row in the CSV file
            for row in csv_reader:
                keyword = row[0].title()
                city = row[1].title()
                state = row[2].upper()
                page_title = create_page_title(keyword, city, state)

                page_data_dict[page_title] = {
                    "keyword": keyword,
                    "city": city,
                    "state": state
                }
        company_name = input("Enter company name: ")
        
        # Proceed with the rest of the original code
    count = 0

    


    website_question = input("Does this company have a website? (y/n):")

    if website_question == "y":

        company_website_input = input("Enter website URL: ")
        company_website = f"Use this website for information: {company_website_input}"

    else:
        company_website = ""

    note_question = input("Do you have anything the AI needs to know about the content output or client? (y/n): ")
    if note_question == "y":
        notes_input = input("Enter notes for the AI: ")
        notes = f"{notes_input}."
    else:
        notes = ""

    # Get user input for section headings
    user_input = input("Enter '1' to manually enter section headings, '2' to use the default section headings, or '3' to use ChatGPT to generate the headings: ")

    if user_input == '1':

        num_sections = int(input("Enter the number of sections for the page: "))
        print("You can use these placeholders: '{keyword}', '{city}', or '{state}' in your manual titles to be used across all items.")
        if data_source == "1":
            same_titles_for_all = ""

        else:
            same_titles_for_all = input("Do you want to use the same titles for all of the items in the csv file? (y/n): ")
        section_titles = []
        for i in range(num_sections):
            section_title = input(f"Enter section {i+1} title: ")
            section_titles.append(section_title)

    elif user_input == '2':
        section_titles = ["Stunning {keyword} In {city}, {state}", 
                            "What Are {keyword}?", 
                            "Why Purchase {keyword} In {city}, {state}?",
                            "What Is The Price Of {keyword} In {city}, {state}?",
                            "Should I Get A {keyword} In {city}, {state}?",
                            "Get The World's Best {keyword} Here In {city}, {state}"]

    elif user_input == '3':
        num_sections = int(input("Enter the number of sections for the page: "))
        section_titles = generate_outline("", "", "", "", "", num_sections)


    print("Running script...")
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("Be Patient - This Can Take A Few Minutes To Start")
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    # Generate or get outline for each page
    for page_title, page_data in page_data_dict.items():
        keyword = page_data["keyword"]
        city = page_data["city"]
        state = page_data["state"]
        page_title = create_page_title(keyword, city, state)

        if user_input == '1':
            outline = []
            for i in section_titles:
                formatted_title = replace_placeholders(i, keyword, city, state).title()
                outline.append(formatted_title)
            page_data["outline"] = outline

        elif user_input == "2":
            outline = []
            for i in section_titles:
                formatted_title = replace_placeholders(i, keyword, city, state).title()
                outline.append(formatted_title)
            page_data["outline"] = outline

        elif user_input == "3":
            outline = generate_outline(page_title, company_name, keyword, city, state, num_sections)
            while create_page_title(keyword, city, state) in outline:
                outline.remove(create_page_title(keyword, city, state))

                        # Remove hierarchical headings from outline
            outline = [section.replace(section.split(". ")[0] + ". ", "") for section in outline]

            page_data["outline"] = outline

    # Create output directory
    output_dir = f"{company_name} Landing Page Content"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Generate content for each page and export to text file
    for page_title, page_data in page_data_dict.items():
        total_page = len(page_data_dict)
        count += 1  # Increment the counter by 1
        print(f"{count}/{total_page} : Generating content for {page_title}")
        outline = page_data["outline"]
        content = create_page_content(page_title, page_data, outline, company_name, page_data["keyword"], page_data["city"], page_data["state"], notes, company_website)

        output_filename = os.path.join(output_dir, f"{page_title}.txt")
        with open(output_filename, "w") as output_file:
            output_file.write(content)

        print(f"Content saved to {output_filename}")

    print("All pages generated successfully!")

if __name__ == '__main__':
    main()


