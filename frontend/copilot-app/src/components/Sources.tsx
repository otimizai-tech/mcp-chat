import React from 'react';

interface Source {
  id: string;
  name: string;
}

interface DataSourceProps {
  sources: Source[];
}

// Function to generate random pastel colors
const generateRandomColor = (): string => {
  // Generate pastel colors by using higher base values
  const r = Math.floor(Math.random() * 127) + 128;
  const g = Math.floor(Math.random() * 127) + 128;
  const b = Math.floor(Math.random() * 127) + 128;
  
  return `rgb(${r}, ${g}, ${b})`;
};

// Function to get contrasting text color (black or white) based on background
const getContrastColor = (bgColor: string): string => {
  // Extract RGB values from the format "rgb(r, g, b)"
  const rgb = bgColor.match(/\d+/g);
  if (!rgb || rgb.length < 3) return 'black';
  
  const r = parseInt(rgb[0]);
  const g = parseInt(rgb[1]);
  const b = parseInt(rgb[2]);
  
  // Calculate luminance - if bright background use dark text, otherwise light text
  const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
  return luminance > 0.5 ? 'black' : 'white';
};

const DataSource: React.FC<DataSourceProps> = ({ sources }) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-4 max-w-md">
      <h3 className="text-lg font-semibold mb-3 text-gray-800">Data Source</h3>
      
      <div className="flex flex-wrap gap-2">
        {sources.map((source) => {
          const bgColor = generateRandomColor();
          const textColor = getContrastColor(bgColor);
          
          return (
            <div 
              key={source.id}
              className="w-10 h-10 rounded flex items-center justify-center cursor-pointer hover:opacity-90 transition-opacity"
              style={{ backgroundColor: bgColor, color: textColor }}
              title={source.name}
            >
              <span className="font-bold text-sm">
                {source.name.charAt(0).toUpperCase()}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default DataSource;