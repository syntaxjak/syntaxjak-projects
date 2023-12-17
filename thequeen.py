import os
import random
import time

class Organism:
    def __init__(self, name, base_path='/home/killswitch/Documents/organisms'):
        self.name = name
        self.is_alive = True
        self.path = os.path.join(base_path, name)  # Set a base path for file operations

        # Create organism's profile as directory
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    # Function to safely remove an organism's directory by deleting all its contents first
    def _remove_organism_directory(self):
        if os.path.exists(self.path):
            # Remove all files in the directory
            for file in os.listdir(self.path):
                file_path = os.path.join(self.path, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            # Remove the directory itself
            os.rmdir(self.path)

    def live(self):
        # Live function to represent the organism's life.
        open(os.path.join(self.path, 'heartbeat.txt'), 'a').close()

    def interact(self, other_organism):
        # Skip interaction if the other organism is the same as this one or is dead
        if self == other_organism or not other_organism.is_alive:
            return

        # Interaction logic here. This could be anything from feeding, fighting, or moving.
        interaction_type = random.choice(['feed', 'fight', 'move'])
        if interaction_type == 'feed':
            # Feed interaction: Create a file to represent feeding.
            with open(os.path.join(self.path, f'feeding_{other_organism.name}.txt'), 'w') as f:
                f.write(f'{self.name} is feeding on {other_organism.name}\n')
        elif interaction_type == 'fight':
            # Fight interaction: Remove the other organism's directory if it 'loses' the fight.
            if random.choice([True, False]):  # Simplified fight outcome
                other_organism.is_alive = False
                other_organism._remove_organism_directory()
        elif interaction_type == 'move':
            # Move interaction: Rename the directory to represent moving to a new location.
            new_name = f"{self.name}_{random.randint(1, 100)}"
            new_path = os.path.join('/home/killswitch/Documents/organisms/host', new_name)
            os.rename(self.path, new_path)
            self.name = new_name
            self.path = new_path

# Create a small ecosystem
ecosystem = [Organism(f'org_{i}') for i in range(5)]

# Corrected simulation loop that handles the scenario when there are no other organisms alive
simulation_steps = 10
for step in range(simulation_steps):
    for org in ecosystem:
        if org.is_alive:
            org.live()  # Represent the organism's life
            # Get a list of other alive organisms excluding the current one
            other_alive_organisms = [o for o in ecosystem if o != org and o.is_alive]
            # If there are no other alive organisms, skip the interaction
            if other_alive_organisms:
                other_org = random.choice(other_alive_organisms)
                org.interact(other_org)  # Interact with other organisms

    time.sleep(1)  # Pause for a bit to simulate time passing

# Clean up created directories at the end of the simulation
#for org in ecosystem:
#    org._remove_organism_directory()

print("Simulation complete.")
