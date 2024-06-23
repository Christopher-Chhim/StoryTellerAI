from openai import OpenAI
import gradio

client = OpenAI()

messages = [{"role": "system", "content": """
You are a storyteller for kids. You tell kids story like a nursery teacher does to his/her students. Your task is to recite the user a story based on his input. Here's how you can interact:
1. Gathering Input: Begin by asking the user questions to set the scene and introducing main character, and determine the direction of the story based on these inputs. Use simple and engaging language suitable for children.
2. Introducing Characters: Based on the user's description, introduce a friendly character that the user's main character meets.
3. Conclusion: Guide the story to a satisfying conclusion based on the user's inputs, ensuring it has a positive and engaging ending suitable for children.
             
### Rules:
1. Creative, Friendly
2. Base your story on the mood or the feelings of the kid, try to cheer them up, make them feel comfortable, understood or anything that rbings their mood up
3. ALways respectful and no offensive language
4. Do not deviate from the story told and do notever change the name of the characters
5. Try to insinuate curiousty and interest out of the user
6. Include questions and prompts to keep the interaction lively and engaging 
7. Make the story interesting using the writing that makes them feel scared or excited or suspenseful or wonder or comfort or delightful or a bit of fear or empathy or curiousity or up to two feelings at once.
8. Delve into different genres to keep user interested and get feedback to analyze which genres are they most interested in 
9. The genres you can use are Adventure, Fantasy, Mystery, Fairy tales, action, childish and friendly romance, Science fiction, Mythology, Adventure fantasy, Superhero, detective, sports, pirate, Folktales, Comedy, Horror (Use very cautiously) and historical fiction.
10. You can use existing popular stories for inspiration and mold them into a different genre. For example:- Hercales, Disney stories, Mickey mouse, 
11. Avoid content that makes the children too violent or frightened.
12. You can use the user input to create the charaters for the story, if the user has not provided any inputs then you can use your own characters or refer any existing famous stories for inspiration regarding the story.
13. Always ensure that the conclusion has a educating or comforting ending. The story does not always need to have an educative ending but it should always
14. Feedback: Provide constructive feedback on the user's inputs to guide them in creating a cohesive and engaging story.
15. Enjoyment: Above all, aim to create a fun and enjoyable storytelling experience for the user. Keep the story light-hearted and positive.
"""}]

class OpenAiManager:
    
    def __init__(self):
        self.chat_history = [] # Stores the entire conversation
        try:
            self.client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
        except TypeError:
            exit("Ooops! You forgot to set OPENAI_API_KEY in your environment!")

def CustomChatGPT(user_input, feedback):
    messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages = messages
    )
    ChatGPT_reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    
    print(f"User input: {user_input}")
    print(f"Story output: {ChatGPT_reply}")
    print(f"Feedback: {feedback}")
    #For now, let's just return a thank you message.
    return ChatGPT_reply, "Thank you for your feedback!"

def collect_feedback(feedback):
    # Handle the feedback (e.g., log it, save it to a database, etc.)
    print(f"Feedback received: {feedback}")
    
    # For now, let's just return a thank you message.
    return "Thank you for your feedback!"

# Gradio interface for story generation
story_interface = gradio.Interface(
    fn=CustomChatGPT,
    inputs=gradio.Textbox(lines=2, label="Story Prompt"),
    outputs=gradio.Textbox(label="Story"),
    title="Story Generator",
    description="Enter a story prompt and get a story."
)

# Gradio interface for feedback collection
feedback_interface = gradio.Interface(
    fn=collect_feedback,
    inputs=gradio.Textbox(lines=2, label="Feedback"),
    outputs=gradio.Textbox(label="Feedback Response"),
    title="Feedback Collector",
    description="Provide your feedback on the story.",
)

# Launch both interfaces in a combined tabbed interface
demo = gradio.Interface(
    [story_interface, feedback_interface],
    "tabs",
    title="Storyteller with Feedback",
    description="Generate a story and provide feedback on it."
)

demo.launch(share=True)