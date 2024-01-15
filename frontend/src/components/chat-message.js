// Inspired by Chatbot-UI and modified to fit the needs of this project
// @see https://github.com/mckaywrigley/chatbot-ui/blob/main/components/Chat/ChatMessage.tsx

import React, { useState, useEffect } from "react";

const Typewriter = ({ text, delay }) => {
  const [currentText, setCurrentText] = useState("");
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    if (currentIndex < text.length) {
      const timeout = setTimeout(() => {
        setCurrentText((prevText) => prevText + text[currentIndex]);
        setCurrentIndex((prevIndex) => prevIndex + 1);
      }, delay);

      return () => clearTimeout(timeout);
    }
  }, [currentIndex, delay, text]);

  return <span>{currentText}</span>;
};

export default Typewriter;
export const ChatMessage = ({ message }) => {
  function UserIcon() {
    return (
      <div className="flex h-8 w-8 shrink-0 select-none items-center justify-center rounded-md border shadow bg-background text-gray-500">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 256 256"
          fill="currentColor"
          className="h-4 w-4"
          strokeWidth={1.5}
        >
          <path d="M230.92 212c-15.23-26.33-38.7-45.21-66.09-54.16a72 72 0 1 0-73.66 0c-27.39 8.94-50.86 27.82-66.09 54.16a8 8 0 1 0 13.85 8c18.84-32.56 52.14-52 89.07-52s70.23 19.44 89.07 52a8 8 0 1 0 13.85-8ZM72 96a56 56 0 1 1 56 56 56.06 56.06 0 0 1-56-56Z"></path>
        </svg>
      </div>
    );
  }

  function SystemIcon() {
    return (
      <div className="flex h-8 w-8 shrink-0 select-none items-center justify-center rounded-md border">
        <img src="/apple-touch-icon.png" />
      </div>
    );
  }

  return (
    <div className="pt-4">
      <div className="mx-auto max-w-2xl px-4">
        <div className="rounded-lg border bg-background p-8">
          <div className="group relative mb-4 flex items-start">
            <div className="flex h-8 w-8 shrink-0 select-none items-center justify-center rounded-md border shadow bg-primary text-primary-foreground">
              <UserIcon />
            </div>
            <div className="flex-1 px-1 ml-4 space-y-2 overflow-hidden">
              {message.question}
            </div>
          </div>
          <div className="border-b mb-6 mt-6"></div>
          <div className="group relative mb-4 flex items-start">
            <div className="flex h-8 w-8 shrink-0 select-none items-center justify-center rounded-md border shadow bg-background">
              <SystemIcon />
            </div>
            <div className="flex-1 px-1 ml-4 space-y-2 overflow-hidden">
              <Typewriter text={message.response} delay={20} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
