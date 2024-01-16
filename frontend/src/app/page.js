"use client";
import { useState, useRef, useEffect } from "react";
import { ChatMessage } from "@/components/chat-message";

const apiUrl = "http://127.0.0.1:5000/api/chat";

export default function Home() {
  const [chats, setChats] = useState([]);
  const [question, setQuestion] = useState("");

  const ref = useRef(null);

  useEffect(() => {
    if (chats.length) {
      ref.current?.scrollIntoView({
        behavior: "smooth",
        block: "end",
      });
    }
  }, [chats.length]);

  const handleSendQuestion = async () => {
    if (!question.trim()) {
      // no need to send an empty message
      return;
    }

    try {
      // send a request to the API with the new question
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: question }),
      });

      if (!response.ok) {
        throw new Error("Failed to send send the question");
      }

      // parse the response and update responses
      const data = await response.json();
      setChats([...chats, data]);

      setQuestion("");
    } catch (error) {
      console.error("Error sending the question:", error.message);
    }
  };

  function ButtonLink({ children }) {
    return (
      <button
        className="inline-flex items-center justify-center rounded-md ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 underline-offset-4 shadow-none hover:underline h-auto p-0"
        onClick={() => setQuestion(children)}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 256 256"
          fill="currentColor"
          className="h-4 w-4 mr-2 text-muted-foreground"
        >
          <path d="m221.66 133.66-72 72a8 8 0 0 1-11.32-11.32L196.69 136H40a8 8 0 0 1 0-16h156.69l-58.35-58.34a8 8 0 0 1 11.32-11.32l72 72a8 8 0 0 1 0 11.32Z"></path>
        </svg>
        {children}
      </button>
    );
  }

  function Welcome() {
    return (
      <div className="pt-4 md:pt-10">
        <div className="mx-auto max-w-2xl px-4">
          <div className="rounded-lg border bg-background p-8">
            <h1 className="mb-2 text-lg font-semibold">
              Welcome to Smart AI Tutor!
            </h1>
            <p className="mb-8 leading-normal text-muted-foreground">
              Your Virtual Learning Companion. Built for Introduction to AI -
              COM727.
            </p>
            <p className="leading-normal text-muted-foreground">
              You can start a conversation here or try the following examples:
            </p>
            <div className="mt-4 flex flex-col items-start space-y-2 font-medium">
              <ButtonLink>What is Artificial Intelligence</ButtonLink>
              <ButtonLink>Could you explain Machine Learning?</ButtonLink>
              <ButtonLink>What are Decision Trees?</ButtonLink>
              <ButtonLink>
                How does the Decision Tree algorithm work?
              </ButtonLink>
              <ButtonLink>What is K-Means Clustering</ButtonLink>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <main className="flex flex-1 flex-col">
      <div className="relative flex min-h-full overflow-hidden">
        <div className="w-full overflow-auto pl-0">
          <div className="pb-[200px]">
            {chats.length ? (
              chats.map((chat, index) => (
                <div key={index}>
                  <ChatMessage message={chat} />
                  {index < chats.length - 1 && <div className="my-4 md:my-8" />}
                </div>
              ))
            ) : (
              <Welcome />
            )}
          </div>
          <div ref={ref}></div>

          {/** chat box */}
          <div className="fixed inset-x-0 bottom-0 w-full bg-gradient-to-b from-muted/30 from-0% to-muted/30 to-50% animate-in duration-300 ease-in-out dark:from-background/10 dark:from-10% dark:to-background/80 peer-[[data-state=open]]:group-[]:lg:pl-[250px] peer-[[data-state=open]]:group-[]:xl:pl-[300px]">
            <div className="mx-auto sm:max-w-2xl sm:px-4">
              <div className="flex h-12 items-center justify-center"></div>
              <div className="space-y-4 border-t bg-background px-4 py-2 shadow-lg sm:rounded-t-xl sm:border md:py-4">
                <div className="relative flex max-h-60 w-full grow flex-col overflow-hidden bg-background px-2 sm:rounded-md sm:border sm:px-2">
                  <textarea
                    name="message"
                    tabIndex={0}
                    rows={1}
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.keyCode == 13 && e.shiftKey == false) {
                        e.preventDefault();
                        handleSendQuestion();
                        return false;
                      }
                    }}
                    placeholder="Send a message."
                    spellCheck={true}
                    className="min-h-[60px] w-full resize-none bg-transparent px-4 py-[1.3rem] focus-within:outline-none"
                  />
                  <div className="absolute right-0 top-4 sm:right-4">
                    <button
                      className="inline-flex items-center justify-center rounded-full text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground shadow-md hover:bg-primary/90 h-8 w-8 p-0"
                      type="submit"
                      data-state="closed"
                      onClick={handleSendQuestion}
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 256 256"
                        fill="currentColor"
                        className="h-4 w-4"
                      >
                        <path d="M200 32v144a8 8 0 0 1-8 8H67.31l34.35 34.34a8 8 0 0 1-11.32 11.32l-48-48a8 8 0 0 1 0-11.32l48-48a8 8 0 0 1 11.32 11.32L67.31 168H184V32a8 8 0 0 1 16 0Z"></path>
                      </svg>
                      <span className="sr-only">Send message</span>
                    </button>
                  </div>
                </div>
                <p className="px-2 text-center text-xs leading-normal text-muted-foreground hidden sm:block">
                  &copy; {new Date().getFullYear()} Smart AI Tutor.{" "}
                  <span className="font-semibold">
                    Introduction to AI - COM727
                  </span>
                  .
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
