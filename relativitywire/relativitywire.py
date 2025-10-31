from manim import *

class NonRelativisticWireScene(Scene):
    def construct(self):
        # Wire (as a rectangle)
        wire = Rectangle(width=20, height=1, fill_color=GRAY, fill_opacity=0.3)
        self.add(wire)

        #observer electron (bottom)
        
        # Protons (upper half)
        protons = VGroup()
        for i in range(5):
            proton = Circle(radius=0.05, color=RED, fill_opacity=1)
            proton.move_to([i - 2, 0.15, 0])
            protons.add(proton)
        self.add(protons)
        # Electrons (lower half)
        electrons = VGroup()
        electron_minus_signs = VGroup()
        for i in range(5):
            electron = Circle(radius=0.05, color=BLUE, fill_opacity=1)
            electron.move_to([i - 2, -0.15, 0])
            minus_sign = Tex("-").scale(0.5).move_to(electron.get_center())
            electrons.add(electron)
            electron_minus_signs.add(minus_sign)
        self.add(electrons, electron_minus_signs)
        electron = Circle(radius=0.05, color=BLUE, fill_opacity=1)
        electron.move_to([-1, -0.9, 0])
        minus_sign = Tex("-").scale(0.5).move_to(electron.get_center())
        electrons.add(electron)
        electron_minus_signs.add(minus_sign)
        self.add(electrons, electron_minus_signs)


        # Distance brackets (d) between adjacent particles in the non-relativistic scene
        # Use two adjacent electrons on the wire (ignore the extra below-wire electron at index 5)
        if len(electrons) >= 3:
            e_left = electrons[1]
            e_right = electrons[2]
            e_brace = BraceBetweenPoints(e_left.get_center(), e_right.get_center(), direction=DOWN)
            e_label = Tex("d").scale(0.6)
            e_label.add_updater(lambda m: m.next_to(e_brace, DOWN, buff=0.1))

            def update_e_brace(m):
                m.become(BraceBetweenPoints(e_left.get_center(), e_right.get_center(), direction=DOWN))
            e_brace.add_updater(lambda m, dt: update_e_brace(m))
            self.add(e_brace, e_label)



            
        #plus signs in protons
        for proton in protons:
            plus_sign = Tex("+").scale(0.3).move_to(proton.get_center())
            self.add(plus_sign)
        
        # Electron flow: slow drift to the right + spawning
        speed = 0.2  # units per second
        d = 1.0  # distance between electrons (spacing from initial positions)
        
        # Track last spawn position (initialize to leftmost electron position)
        last_spawn_x = [-3]  # leftmost electron starts at x = -2
        
        def create_electron_pair(x_pos):
            """Create an electron and its minus sign at given x position"""
            electron = Circle(radius=0.05, color=BLUE, fill_opacity=1)
            electron.move_to([x_pos, -0.15, 0])
            minus_sign = Tex("-").scale(0.5).move_to(electron.get_center())
            return electron, minus_sign
        
        def drift_and_spawn(mob, dt):
            # Drift all electrons to the right
            mob.shift(RIGHT * speed * dt)
        
        def drift_right(mob, dt):
            # Drift all electrons to the right
            mob.shift(RIGHT * speed * dt)
        
        def check_and_spawn(dt):
            # Get leftmost electron's x position
            if len(electrons) > 0:
                leftmost_x = min(e.get_center()[0] for e in electrons)
                
                # Check if leftmost electron has moved d from last spawn position
                if leftmost_x >= last_spawn_x[0] + d:
                    # Spawn new electron d to the left of current leftmost
                    new_x = leftmost_x - d
                    new_electron, new_minus_sign = create_electron_pair(new_x)
                    
                    # Add to VGroups (they're already added to scene, so new items appear automatically)
                    electrons.add(new_electron)
                    electron_minus_signs.add(new_minus_sign)
                    
                    # Update last spawn position
                   # last_spawn_x[0] = leftmost_x
        
        # Combined updater that both drifts and checks for spawning
        def combined_updater(mob, dt):
            # Always drift electrons (including newly spawned ones)
            drift_right(electrons, dt)
            drift_right(electron_minus_signs, dt)
            # Check for spawning
            check_and_spawn(dt)
        
        # Create a tracker object for the combined updater
        tracker = VGroup()
        tracker.add_updater(combined_updater)
        self.add(tracker)
        
        # Also add updaters to the electron groups for continuous drift
        electrons.add_updater(drift_right)
        electron_minus_signs.add_updater(drift_right)
        
        self.wait(8)
        
        electrons.remove_updater(drift_right)
        electron_minus_signs.remove_updater(drift_right)
        tracker.remove_updater(combined_updater)
        self.wait()

class RelativisticWireScene(Scene):
    def construct(self):
        # Wire (as a rectangle)
        wire = Rectangle(width=20, height=1, fill_color=GRAY, fill_opacity=0.3)
        self.add(wire)

        # Parameters
        base_spacing = 1
        factor = 1.5
        electron_spacing = base_spacing * factor   # reduced spacing
        proton_spacing = base_spacing / factor     # increased spacing
        speed = 0.2  # match NonRelativisticWireScene electron drift speed

        # Electrons (stationary, lower half)
        electrons = VGroup()
        electron_minus_signs = VGroup()
        for i in range(8):
            x = (i - 2) * electron_spacing
            electron = Circle(radius=0.05, color=BLUE, fill_opacity=1)
            electron.move_to([x, -0.15, 0])
            minus_sign = Tex("-").scale(0.5).move_to(electron.get_center())
            electrons.add(electron)
            electron_minus_signs.add(minus_sign)
        self.add(electrons, electron_minus_signs)
        electron = Circle(radius=0.05, color=BLUE, fill_opacity=1)
        electron.move_to([0, -0.9, 0])
        minus_sign = Tex("-").scale(0.5).move_to(electron.get_center())
        electrons.add(electron)
        electron_minus_signs.add(minus_sign)
        self.add(electrons, electron_minus_signs)

        # Protons (move backward/left at same speed, upper half)
        protons = VGroup()
        proton_plus_signs = VGroup()
        for i in range(14):
            x = (i -4) * proton_spacing
            proton = Circle(radius=0.05, color=RED, fill_opacity=1)
            proton.move_to([x, 0.15, 0])
            plus_sign = Tex("+").scale(0.3).move_to(proton.get_center())
            protons.add(proton)
            proton_plus_signs.add(plus_sign)
        self.add(protons, proton_plus_signs)

        # Protons drift left (backwards) at the specified speed
        def drift_left(mob, dt):
            mob.shift(LEFT * speed * dt)

        protons.add_updater(drift_left)
        proton_plus_signs.add_updater(drift_left)

        self.wait(8)

        protons.remove_updater(drift_left)
        proton_plus_signs.remove_updater(drift_left)
        self.wait()
