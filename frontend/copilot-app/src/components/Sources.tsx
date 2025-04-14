import React from "react";

interface Source {
  id: string;
  name: string;
}

interface DataSourceProps {
  sources: Source[];
}

// Function to get color based on the first letter (A-Z)
const getLetterColor = (letter: string): string => {
  const normalizedLetter = letter.toLowerCase();

  // Color map for each letter
  const letterColors: { [key: string]: string } = {
    a: "rgb(255, 179, 179)", // Light red
    b: "rgb(255, 223, 179)", // Light orange
    c: "rgb(255, 255, 179)", // Light yellow
    d: "rgb(204, 255, 179)", // Light lime
    e: "rgb(179, 255, 179)", // Light green
    f: "rgb(179, 255, 204)", // Light mint
    g: "rgb(179, 255, 230)", // Light teal
    h: "rgb(179, 230, 255)", // Light sky blue
    i: "rgb(179, 204, 255)", // Light blue
    j: "rgb(204, 179, 255)", // Light lavender
    k: "rgb(230, 179, 255)", // Light purple
    l: "rgb(255, 179, 255)", // Light magenta
    m: "rgb(255, 179, 230)", // Light pink
    n: "rgb(255, 204, 179)", // Light peach
    o: "rgb(255, 230, 179)", // Light amber
    p: "rgb(230, 255, 179)", // Light chartreuse
    q: "rgb(179, 255, 191)", // Light jade
    r: "rgb(179, 255, 217)", // Light aquamarine
    s: "rgb(179, 242, 255)", // Light azure
    t: "rgb(179, 191, 255)", // Light periwinkle
    u: "rgb(217, 179, 255)", // Light violet
    v: "rgb(242, 179, 255)", // Light fuchsia
    w: "rgb(255, 179, 217)", // Light rose
    x: "rgb(255, 217, 179)", // Light coral
    y: "rgb(242, 255, 179)", // Light lemon
    z: "rgb(191, 255, 179)", // Light mint green
  };

  // Return the color for the letter or a default color if letter not found
  return letterColors[normalizedLetter] || "rgb(200, 200, 200)";
};

// Function to get contrasting text color (black or white) based on background
const getContrastColor = (bgColor: string): string => {
  // Extract RGB values from the format "rgb(r, g, b)"
  const rgb = bgColor.match(/\d+/g);
  if (!rgb || rgb.length < 3) return "black";

  const r = parseInt(rgb[0]);
  const g = parseInt(rgb[1]);
  const b = parseInt(rgb[2]);

  // Calculate luminance - if bright background use dark text, otherwise light text
  const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
  return luminance > 0.5 ? "black" : "white";
};

const DataSource: React.FC<DataSourceProps> = ({ sources }) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-4 max-w-md">
      <h3 className="text-lg font-semibold mb-3 text-gray-800">Data Source</h3>

      <div className="flex flex-wrap gap-2">
        {sources.map((source) => {
          const firstLetter = source.name.charAt(0);
          const bgColor = getLetterColor(firstLetter);
          const textColor = getContrastColor(bgColor);

          return (
            <div
              key={source.id}
              className="w-10 h-10 rounded flex items-center justify-center cursor-pointer hover:opacity-90 transition-opacity"
              style={{ backgroundColor: bgColor, color: textColor }}
              title={source.name}
            >
              <span className="font-bold text-sm">
                {firstLetter.toUpperCase()}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default DataSource;
