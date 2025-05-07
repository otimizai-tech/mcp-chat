import { MessageRole } from "@copilotkit/runtime-client-gql";

interface Message {
  content: string;
  role: MessageRole;
  timestamp: number;
}

interface RawCellProps {
  message: Message;
}

function UserMessage({ content }: { content: string }) {
  return (
    <div className="flex justify-end">
      <div className="max-w-[80%] p-4 rounded-2xl whitespace-pre-wrap break-words bg-blue-500 text-white rounded-br-none">
        <span className="text-base">{content}</span>
      </div>
    </div>
  );
}

function AIMessage({ content }: { content: string }) {
  return (
    <div className="flex justify-start">
      <div className="max-w-[80%] p-4 rounded-2xl whitespace-pre-wrap break-words bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-gray-800 dark:text-gray-200 rounded-bl-none">
        <span className="text-base">{content}</span>
      </div>
    </div>
  );
}

export function RawCell({ message }: RawCellProps) {
  console.log("RawCell rendering message:", {
    content: message.content,
    role: message.role,
    isUser: message.role === MessageRole.User,
  });

  if (message.role === MessageRole.User) {
    return (
      <div className="message-wrapper user">
        <UserMessage content={message.content} />
      </div>
    );
  } else {
    return (
      <div className="message-wrapper ai">
        <AIMessage content={message.content} />
      </div>
    );
  }
}
