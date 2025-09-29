import { 
  ActionPanel, 
  List, 
  Action, 
  useNavigation,
} from "@raycast/api";
import { registerAllPlugins, PluginRegistry } from "./plugins";

// Initialize plugins on module load
registerAllPlugins();

export default function Command() {
  const { push } = useNavigation();
  const categories = PluginRegistry.getCategories();

  return (
    <List searchBarPlaceholder="Search developer tools...">
      {categories.map((category) => {
        const tools = PluginRegistry.getToolsByCategory(category.key);
        
        return (
          <List.Section key={category.key} title={category.name}>
            {tools.map((tool) => (
              <List.Item
                key={tool.key}
                icon={tool.icon}
                title={tool.name}
                subtitle={tool.description}
                keywords={tool.keywords}
                actions={
                  <ActionPanel>
                    <Action
                      title="Open Tool"
                      onAction={() => push(<tool.component />)}
                    />
                  </ActionPanel>
                }
              />
            ))}
          </List.Section>
        );
      })}
    </List>
  );
}