import { useCopilotAction, useCopilotReadable } from "@copilotkit/react-core";
import { createContext, useContext, useState, ReactNode } from "react";

export interface Source {
  id: string;
  name: string;
}

const defaultSources: Source[] = [
  { id: '1', name: 'Google' },
  { id: '2', name: 'Facebook' },
  { id: '3', name: 'Twitter' }
];

let nextId = defaultSources.length + 1;

type SourcesContextType = {
  sources: Source[];
  addSource: (name: string) => void;
  deleteSource: (id: string) => void;
};

const SourcesContext = createContext<SourcesContextType | undefined>(undefined);

export const SourcesProvider = ({ children }: { children: ReactNode }) => {
  const [sources, setSources] = useState<Source[]>(defaultSources);

  useCopilotReadable({
    description: "The list of available data sources",
    value: JSON.stringify(sources),
  });

  useCopilotAction({
    name: "addSource",
    description: "Adds a new data source to the list",
    parameters: [
      {
        name: "name",
        type: "string",
        description: "The name of the data source",
        required: true,
      },
    ],
    handler: ({ name }) => {
      addSource(name);
    }
  });

  useCopilotAction({
    name: "deleteSource",
    description: "Deletes a data source from the list",
    parameters: [
      {
        name: "id",
        type: "string",
        description: "The id of the data source",
        required: true,
      },
    ],
    handler: ({ id }) => {
      deleteSource(id);
    }
  });

  const addSource = (name: string) => {
    setSources([...sources, { id: String(nextId++), name }]);
  };

  const deleteSource = (id: string) => {
    setSources(sources.filter((source) => source.id !== id));
  };

  return (
    <SourcesContext.Provider value={{ sources, addSource, deleteSource }}>
      {children}
    </SourcesContext.Provider>
  );
};

export const useSourceManager = () => {
  const context = useContext(SourcesContext);
  if (context === undefined) {
    throw new Error("useSourceManager must be used within a SourcesProvider");
  }
  return context;
};
