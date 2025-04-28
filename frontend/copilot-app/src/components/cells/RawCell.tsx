import { Typewriter } from 'react-simple-typewriter';

interface RawCellProps {
  metadata: Record<string, any>;
  source: string[];
  isUser: boolean;
  onClick?: () => void;
}

export function RawCell({ source, isUser, onClick }: RawCellProps) {
  const message = source[0].replace(/^(User|model): /, '');
  
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-[80%] p-4 rounded-2xl whitespace-pre-wrap break-words ${
          isUser
            ? 'bg-blue-500 text-white rounded-br-none'
            : 'bg-white border border-gray-200 text-gray-800 rounded-bl-none'
        }`}
        onClick={onClick}
      >
        {isUser ? (
          <span className="text-base">{message}</span>
        ) : (
          <span className="text-base">
            <Typewriter
              words={[message]}
              cursor={false}
              cursorStyle="_"
              typeSpeed={10}
              delaySpeed={1000}
            />
          </span>
        )}
      </div>
    </div>
  );
}
