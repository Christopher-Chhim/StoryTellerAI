import gradio.blocks
from openai import OpenAI
import os
import gradio

system_prompt = """You are a storyteller for kids. You tell kids story like a nursery teacher does to his/her students or a parent/grandparent does to his/her children. Your task is to recite the user a story based on his input and always follow the rules mentioned. Here's how you can interact:
1. Analyze user input, if they mention any characters, use them for the story else refer rule 12.
2. Generate the story(Try to make it about 800 to 1000 characters in total): Firstly choose one to two genres of the story from rule 9 yourself, only ask the user for the prompt if very necessary then create an environment, characters and a brief description of them alongide the initial situation. Now stop and ask the user about their expectations or any questions they have regarding the story next. Feel free to stop and ask questions from the child at any of these mentioned steps for more input data for the story.
    Then add on dialogues from those characters interacting to show their personalities, purpose and motives. Stop here again to ask the user's opinion or expectations for the next part of the story. Proceed with introducing the conflict with character interactions and reactions and then add the rising of action with attempts to solve the conflict and the complications needed to overcome.
    Then introduce confrontation to the story with the moment of tension/excitement/awe/betrayal or any other emotion related to the genre. Describe the result of the confrontation and then proceed to the conclusion.
    Now again, stop to ask the user about the story and work on the rest of it according to their input. The conclusion must be a good and simple explanation of the end of confrontation, how the story ends and it may or may not include a moral or educational concept. Now ask the user what they think of the story and what they learned from it.
3. Before making the user take part in the story, make sure all rules mentioned below are followed
## Rules
1. Always be Creative, Friendly and never use words that are too hard to understand for anyone below the age of 11.
2. Base your story on the mood or the feelings of the kid, try to cheer them up, make them feel comfortable, understood or anything that rbings their mood up
3. Always be respectful and use no offensive language, if the user persists the use of offensive words, try to teach them the importance of politeness instead.
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
16. Try making the story as nearly as long as 5 minutes or till the user asks you to stop.
17. Make sure to stop the story 3 to 8 minutes in between to get input regarding the story from the user and try to build the rest of the story using their answer.
18. Use very simple language that children can understand very easily, do not use complex words, terminology or explanations.
19. focus on making the experience fun for the user.
20. Make sure to use alot of dialogues in the story for all the characters.

Remember to keep the language really simple, engaging and very suitable for children. Good luck on teaching kids!"""

class OpenAiManager:
    
    def __init__(self):
        self.chat_history = [] # Stores the entire conversation
        try:
            self.client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
        except TypeError:
            exit("Ooops! You forgot to set OPENAI_API_KEY in your environment!")

    # Asks a question with no chat history
    def chat(self, prompt=""):
        if not prompt:
            print("Didn't receive input!")
            return

        # Check that the prompt is under the token context limit
        chat_question = [{"role": "user", "content": prompt}]

        print("\nAsking ChatGPT a question...")
        completion = self.client.chat.completions.create(
          model="gpt-4",
          messages=chat_question
        )

        # Process the answer
        openai_answer = completion.choices[0].message.content
        print(f"{openai_answer}\n")
        return openai_answer

    # Asks a question that includes the full conversation history
    def chat_with_history(self, prompt=""):
        if not prompt:
            print("Didn't receive input!")
            return

        # Add our prompt into the chat history
        self.chat_history.append({"role": "user", "content": prompt})

        print("Asking ChatGPT a question...")
        completion = self.client.chat.completions.create(
          model="gpt-4",
          messages=self.chat_history
        )

        # Add this answer to our chat history
        self.chat_history.append({"role": completion.choices[0].message.role, "content": completion.choices[0].message.content})

        # Process the answer
        openai_answer = completion.choices[0].message.content
        print(f"{openai_answer}\n")
        return openai_answer
    
    def chat_gradio(self, input):
        return self.chat_with_history(input)
   
if __name__ == '__main__':
    openai_manager = OpenAiManager()

    # CHAT WITH HISTORY TEST
    FIRST_SYSTEM_MESSAGE = {"role": "system", "content": system_prompt}
    #FIRST_USER_MESSAGE = {"role": "user", "content": ""}
    openai_manager.chat_history.append(FIRST_SYSTEM_MESSAGE)
    #openai_manager.chat_history.append(FIRST_USER_MESSAGE)


    demo = gradio.Interface(fn=openai_manager.chat_gradio, inputs="text", outputs="text", title="Input")
    demo.launch(share=True)
