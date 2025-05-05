interface RawCellProps {
  metadata: Record<string, any>;
  source: string[];
  isUser: boolean;
  onClick?: () => void;
}

export function RawCell({ source, isUser, onClick }: RawCellProps) {
  // More robust handling of undefined or null values
  const message =
    source && Array.isArray(source) && source.length > 0 && source[0]
      ? typeof source[0] === "string"
        ? source[0].replace(/^(User|model): /, "")
        : String(source[0])
      : "";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[80%] p-4 rounded-2xl whitespace-pre-wrap break-words ${
          isUser
            ? "bg-blue-500 text-white rounded-br-none"
            : "bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-gray-800 dark:text-gray-200 rounded-bl-none"
        }`}
        onClick={onClick}
      >
        <span className="text-base">{message}</span>
      </div>
    </div>
  );
}
