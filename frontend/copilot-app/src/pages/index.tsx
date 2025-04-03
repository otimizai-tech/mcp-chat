import { Geist } from "next/font/google";
import Link from 'next/link';

const geist = Geist({
  subsets: ["latin"],
});

export default function Home() {
  return (
    <div className={`${geist.className} min-h-screen flex flex-col items-center justify-center bg-gradient-to-b from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800`}>
      <div className="text-center space-y-8">
        <h1 className="text-4xl font-bold text-gray-800 dark:text-gray-100">
          Welcome to Copilot Chat Otimizai
        </h1>
        
        <p className="text-lg text-gray-600 dark:text-gray-300 max-w-md mx-auto">
          Start a conversation with our AI assistant, from Otimizai
        </p>

        <Link
          href="/copilot_page"
          className="inline-block px-8 py-4 text-lg font-medium text-white bg-blue-600 rounded-full hover:bg-blue-700 transition-colors duration-200 transform hover:scale-105 shadow-lg hover:shadow-xl"
        >
          Start Chat
        </Link>
      </div>

      <footer className="absolute bottom-8 text-sm text-gray-500 dark:text-gray-400">
        Otimizai
      </footer>
    </div>
  );
}
