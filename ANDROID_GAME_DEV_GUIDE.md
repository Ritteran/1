# Android 3D Game Development Guide for Complete Beginners
## Third-Person Adventure + Puzzle Games on Mid-Range Android

---

## A) Reality Check + Assumptions

- **2 hrs/week is extremely limited.** A single polished 3D level with puzzles, camera, and UI can take 40–80+ hours even for experienced devs. At 2 hrs/week, your first shippable micro-game will take ~2–4 months. Accept this pace.
- **"Hyper-realistic" visuals are not feasible** for your situation — not because the engine can't render them, but because creating or even assembling hyper-real assets requires advanced lighting, shader, and optimization skills. Mid-range Android GPUs (Adreno 610–619, Mali-G57) cannot sustain photorealistic rendering at stable framerates. This style also demands multi-GB texture budgets that blow past mobile memory limits (~2–3 GB usable RAM).
- **"Sharp stylized like Zelda"** (cel-shaded, clean geometry, strong color palette) is the correct target. It is forgiving of low poly counts, looks intentional on small screens, and runs well on constrained hardware. Free asset packs (Kenney, KayKit, Quaternius) already provide this style.
- **You will not model your own 3D assets** at the start. That's fine. Kitbashing free CC0 packs is a legitimate strategy used even by professional jam devs.
- **Android thermal throttling is your real enemy**, not raw GPU power. A game that runs at 60 FPS for 10 seconds but drops to 20 FPS after 3 minutes of play has failed. You must test sustained performance, not peak.
- **Scope kills hobby projects.** Your first 3 games should each have 1 level, 1 mechanic, and 1 puzzle. "Shippable" means: launches on phone, plays to completion, doesn't crash.
- **Google Play publishing has friction** (developer account $25 one-time, app review, target API compliance, privacy policy). Plan for this as a dedicated task, not an afterthought.
- **Assumptions made:** You have an Android phone for testing (USB debugging capable). You have stable internet for downloads. You will use your HP Victus as your dev machine. You are comfortable installing software and following tutorials.

---

## B) Engine Recommendation

### 1) Comparison Table

| Criteria | **Unity 6** | **Godot 4.6** | **Unreal Engine 5.5+** | **Defold** |
|---|---|---|---|---|
| **Best for** | Mobile 3D, massive ecosystem | Indie 2D/3D, full ownership | AAA-quality 3D, film-quality visuals | Lightweight 2D, tiny builds |
| **Language / Scripting** | C# | GDScript (Python-like), C#, C++ | Blueprints (visual), C++ | Lua |
| **Android export maturity** | Excellent — battle-tested, one-click build pipeline | Good — improved significantly in 4.5–4.6, full Gradle builds now supported on-device | Functional but heavy — APK sizes large, iteration slow, Vulkan required for modern features | Excellent for 2D — tiny APKs (<5 MB), but 3D tooling is immature |
| **3D workflow quality** | Excellent — prefabs, ProBuilder, Terrain, animation state machine, NavMesh, robust UI (UI Toolkit + uGUI) | Good — nodes/scenes, built-in animation, NavigationServer3D, Control nodes for UI. Less polished than Unity for 3D but rapidly improving | Best-in-class — Nanite, Lumen, Sequencer, world partition. Overkill for mobile and beginners | Minimal — 3D is possible but you build most tooling yourself. Not recommended for 3D-first projects |
| **Performance tooling** | Excellent — Frame Debugger, Profiler (CPU/GPU/Memory), Memory Profiler package, Android Logcat integration | Adequate — built-in profiler, monitors, remote debugger. Less granular than Unity for mobile-specific metrics | Excellent — Unreal Insights, GPU Visualizer, stat commands. But profiling workflow is complex | Basic — built-in profiler exists but limited compared to Unity/Unreal |
| **Learning curve (true beginner)** | Moderate — C# requires learning programming fundamentals, but tutorials are abundant (Unity Learn, YouTube) | Low-Moderate — GDScript is simpler than C#, editor is lighter, but fewer polished 3D-specific tutorials | Steep — Blueprints help avoid code but the editor is overwhelming, build times are long, mobile workflow is painful | Low for 2D — but you'd be fighting the engine for 3D adventure games |
| **Licensing / cost** | **Free** (Personal) if revenue < $200K/year. No runtime fee. No splash screen in Unity 6. Pro: $2,200/seat/year above $200K. ([source](https://unity.com/products)) | **Free forever**, MIT license. No royalties, no restrictions, no splash screen. ([source](https://godotengine.org)) | **Free** until $1M lifetime gross revenue, then 5% royalty (3.5% if publishing on Epic Games Store simultaneously). ([source](https://www.unrealengine.com/en-US/license)) | **Free forever**, source-available (Apache 2.0 derivative). No royalties. ([source](https://defold.com/license/)) |
| **Fit for YOUR constraints** | **Strong fit.** Best mobile 3D ecosystem, most Android tutorials, largest free asset store (Unity Asset Store free section + Fab), reliable build-to-phone workflow. C# is harder than GDScript but more transferable. | **Good fit.** Truly free, lighter editor, GDScript is beginner-friendly. Android export improved greatly in 4.5–4.6. Fewer 3D mobile tutorials and smaller asset ecosystem than Unity. | **Poor fit.** Editor requires 100+ GB disk, builds take minutes, APKs are bloated for simple games. Overkill complexity for a beginner making puzzle games. Nanite/Lumen don't work on mobile. | **Poor fit for 3D.** Excellent engine but 3D tooling is self-built. Would add months of extra work for a 3D third-person game. |

### 2) Final Pick: Start with Unity 6

**Start with Unity 6 (LTS 6.0 or 6.3) because:**

- **Android build pipeline is the most mature** of any engine for 3D mobile games. One-click Build & Run to a connected phone. IL2CPP backend for performance. Built-in Android Logcat for debugging on-device.
- **3D workflow is complete out of the box.** Cinemachine (free) handles third-person cameras. NavMesh handles pathfinding. Animation state machines handle character animation. UI Toolkit or uGUI handles menus. ProBuilder handles basic level geometry. You don't need external tools for any of these.
- **Free asset ecosystem is the largest.** Unity Asset Store has thousands of free 3D assets, and external packs (Kenney, KayKit, Quaternius) all provide Unity-ready imports. Synty Studios periodically offers free stylized packs.
- **Tutorial density is unmatched.** Unity Learn (official, free) has structured pathways. Brackeys (archived but still relevant), Sebastian Lague, Samyam, and hundreds of others cover every topic with video walkthroughs.
- **Performance profiling is built-in and mobile-aware.** Frame Debugger, CPU/GPU Profiler, Memory Profiler, and the Android Logcat package let you diagnose thermal throttling, draw call spikes, and memory pressure without leaving the editor.
- **Licensing is safe.** You will not hit the $200K threshold as a hobby dev. Unity 6 removed the splash screen requirement and the Runtime Fee is dead. Your games are yours.
- **C# is harder to learn than GDScript but is a real-world language** used in enterprise software, web backends, and other engines. Time invested in C# is not wasted.

### 3) Backup Pick: Godot 4.6

**Pick Godot instead if:**

- You find C# too frustrating and want a Python-like scripting language (GDScript)
- You philosophically prefer fully open-source tools with zero licensing risk
- Unity's editor feels too heavy or cluttered for your workflow
- You want a lighter install footprint (Godot editor is ~100 MB vs Unity's multi-GB install)

**Trade-offs to accept with Godot:**
- Fewer 3D mobile-specific tutorials (you'll rely more on docs + forums)
- Smaller free 3D asset ecosystem (though Kenney/KayKit/Quaternius still work)
- Android export has improved greatly but has less battle-testing than Unity's
- No equivalent to Cinemachine for camera systems — you'll code your own

### 4) Starter Setup Checklist (Unity 6)

1. **Install Unity Hub** from [unity.com/download](https://unity.com/download)
2. **Install Unity 6.0 LTS** (6000.0.x) — choose LTS for stability. During install, check:
   - [x] Android Build Support
   - [x] Android SDK & NDK Tools (Unity installs these automatically)
   - [x] OpenJDK (Unity bundles this)
3. **Verify Android toolchain**: Edit → Preferences → External Tools → Android. Confirm SDK, NDK, and JDK paths are populated. Unity handles this if you checked the boxes above.
4. **Create a new project** using the **3D (URP)** template — Universal Render Pipeline is the correct choice for mobile. Do NOT use HDRP (desktop/console only) or Built-in (legacy).
5. **Set target platform**: File → Build Settings → Android → Switch Platform
6. **Connect your Android phone** via USB:
   - Enable Developer Options on phone (Settings → About Phone → tap Build Number 7 times)
   - Enable USB Debugging
   - In Unity: Build Settings → Run Device → select your phone
   - Click "Build and Run" to verify the pipeline works with an empty scene
7. **Install these free packages** (Window → Package Manager):
   - Cinemachine (third-person camera)
   - Input System (new input, better for mobile touch)
   - Android Logcat (on-device debugging)
   - TextMeshPro (UI text)
8. **Project Settings for mobile**:
   - Player → Other Settings → Color Space: Linear
   - Player → Other Settings → Graphics APIs: remove Vulkan if targeting older devices, or keep both (OpenGLES3 fallback)
   - Quality → set a "Mobile" quality level: no real-time shadows initially, 2x MSAA max, LOD bias 1.0
   - Player → Other Settings → Target API Level: Android 14 (API 34) — required by Google Play as of August 2024
9. **Version control**: Initialize a Git repository (see Section F)

---

## C) Visual Style Plan

### Recommended Art Direction: Sharp Stylized (Cel-shaded / Flat-lit)

Think *Zelda: Wind Waker*, *Tunic*, *A Short Hike*, *Genshin Impact (low settings)*. Clean geometry, bold colors, minimal texture detail compensated by strong silhouettes and color contrast.

**Why this works for you:**
- Low-poly models + flat/gradient textures look intentional, not cheap
- Fewer textures = smaller APK, less VRAM, faster load times
- Cel/toon shaders are simple to implement in URP (Shader Graph)
- Free asset packs (Kenney, KayKit, Quaternius) already use this style
- Looks great on small phone screens where detail is lost anyway

**Why hyper-realism is wrong for this project:**
- PBR material authoring (albedo, normal, metallic, roughness, AO) requires Substance Painter or equivalent — paid, complex, slow
- Photorealistic assets demand 2K–4K textures × dozens of meshes = gigabytes of VRAM and storage
- Realistic lighting requires baked lightmaps (long bake times, large file sizes) or real-time GI (not feasible on mobile)
- Any imperfection in realism breaks immersion (uncanny valley); stylized art is forgiving
- Mid-range Android GPUs cannot sustain realistic rendering at playable framerates

### Concrete Performance Targets (Mid-Range Android)

| Metric | Target | Rationale |
|---|---|---|
| **FPS** | 30 FPS locked (sustained) | 60 is ideal but 30 stable is better than 60 unstable. Use `Application.targetFrameRate = 30;` |
| **Triangle budget** | 50K–100K triangles per frame (total scene) | Mid-range GPUs (Adreno 610, Mali-G57) handle this comfortably. Split: ~5K for player, ~3K per interactive object, rest for environment |
| **Draw calls** | < 100 per frame | Use static batching, GPU instancing, texture atlases. URP SRP Batcher helps. |
| **Texture sizes** | 512×512 max for hero assets, 256×256 for props, 128×128 for distant/small objects | Use ASTC compression (Android standard). Avoid uncompressed textures. |
| **APK size** | < 150 MB (ideally < 80 MB for early projects) | Google Play allows up to 150 MB base APK. Use Asset Bundles or Addressables for larger games. |
| **RAM usage** | < 1 GB total | Mid-range devices have 4–6 GB RAM but OS + apps consume 2–3 GB. Stay under 1 GB for your game. |
| **Thermal** | No sustained >80% GPU utilization | Profile with Unity Profiler over 10+ minutes of gameplay. If GPU is pegged, reduce draw calls or resolution. |

### Lighting Approach

- **Use baked lighting for static environments.** Bake lightmaps at low resolution (20–40 texels/unit). This gives you soft shadows and ambient light for free at runtime.
- **One real-time directional light only** (the sun). No real-time point/spot lights unless absolutely necessary.
- **Light Probes** for dynamic objects (player character, moving puzzle pieces) to pick up baked light cheaply.
- **No real-time shadows on mobile initially.** If needed later, use one cascaded shadow map on the directional light only, with a short shadow distance (10–15 meters).

### Post-Processing (URP)

**Use sparingly:**
- Bloom (low intensity) — adds visual polish cheaply
- Color grading / white balance — unifies the look of mixed free assets
- Vignette — cheap, adds focus

**Avoid on mobile:**
- Screen-space ambient occlusion (SSAO) — expensive per-pixel
- Depth of field — expensive, disorienting on small screens
- Motion blur — expensive, nauseating on mobile
- Screen-space reflections — expensive, unnecessary for stylized art

### Animation Tips for "Sharp" Feel

- Use snappy, quick transitions (0.05–0.1s blend times) — not slow, floaty blends
- Anticipation frames before big actions (wind-up before jump, slight crouch before sprint)
- Overshoot on camera movements (Cinemachine damping: low values = snappier)
- Use animation events to trigger SFX/VFX at exact keyframes
- Limit bone count: 30–50 bones for player character, 15–20 for NPCs

### Cut List (What to Remove First if Performance Drops)

Priority order — cut from top first:

1. Real-time shadows → switch to blob shadows (a dark circle under characters)
2. Post-processing → disable all, re-enable one at a time
3. Texture resolution → halve all textures (512→256, 256→128)
4. Particle effects → reduce count by 50%, shorten lifetime
5. Draw distance → reduce camera far clip from 100m to 50m
6. Dynamic objects in scene → reduce NPC/prop count per area
7. Anti-aliasing → drop from 2x MSAA to none
8. Target framerate → lock to 24 FPS (last resort, not ideal)

---

## D) Project Slate (10 Projects)

### Projects 1–3: Starter (Ultra-Small, Shippable)

| # | Project Name | Core Loop | Key Mechanics | Puzzle Hook | What I Learn | Android Risk | MVP "Done" | Stretch Goals | Est. Weeks (2 hrs/wk) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **Cube Walker** | Walk a character through a single room to reach an exit | - 3rd-person controller (move/rotate) | Push a box onto a floor switch to open the door | Character controller, camera setup, basic physics (Rigidbody), Android build pipeline | Low — one room, no AI, minimal assets | Character moves, camera follows, box pushes onto switch, door opens, "You Win" text appears. Runs on phone. | Add a second room; add footstep SFX | 4–5 |
| | | | - Cinemachine 3rd-person follow cam | | | | | | |
| | | | - Box pushing (Rigidbody + collision) | | | | | | |
| | | | - Trigger zone (floor switch) | | | | | | |
| | | | - Scene transition or win screen | | | | | | |
| 2 | **Light the Torches** | Navigate a small courtyard and light 3 torches in the correct order to unlock a gate | - Player movement (reuse from P1) | Torches must be lit in a specific order (clue written on a wall). Wrong order resets them. | Interaction system (press button to act), UI prompts, simple state machine (torch on/off/wrong), particle effects (fire), basic save (PlayerPrefs) | Low — outdoor scene, static lighting, no AI | 3 torches, 1 courtyard, order puzzle works, gate opens, completion screen. Runs on phone. | Add a timer; add a hint system | 4–5 |
| | | | - Interaction system (raycast + UI prompt) | | | | | | |
| | | | - State tracking (which torches lit, in what order) | | | | | | |
| | | | - Particle system (torch fire) | | | | | | |
| | | | - Simple save/load (PlayerPrefs) | | | | | | |
| 3 | **Bridge Builder** | Cross a broken bridge by finding and placing 3 planks hidden in a small island environment | - Item pickup and inventory (collect plank → slot into bridge) | Planks are hidden behind simple environmental obstacles (move a rock, climb a ledge, wade through shallow water) | Inventory system (basic), item placement/snapping, level design with verticality, touch-friendly UI | Low — small environment, no enemies, static scene | 3 planks found, placed on bridge, player crosses, end screen. Runs on phone with touch controls. | Add a collectible counter; add a simple NPC with dialogue | 5–6 |
| | | | - Object snapping (plank → bridge slots) | | | | | | |
| | | | - Basic environmental traversal (ledge, wade) | | | | | | |
| | | | - Touch-optimized UI (inventory bar) | | | | | | |

### Projects 4–7: Skill Builders

| # | Project Name | Core Loop | Key Mechanics | Puzzle Hook | What I Learn | Android Risk | MVP "Done" | Stretch Goals | Est. Weeks (2 hrs/wk) |
|---|---|---|---|---|---|---|---|---|---|
| 4 | **Mirror Temple** | Explore a small temple (3 rooms) and redirect light beams using rotatable mirrors to unlock doors | - Mirror rotation (touch drag or button) | Light beams must hit specific targets. Mirrors reflect at angles. Multiple beams combine in the final room. | Raycasting for light beams, rotation mechanics, multi-room scene design, baked lighting, URP line renderer or shader-based beams | Med — raycasts + line renderers need optimization; test draw calls | 3 rooms, light beam puzzle in each, final door opens, temple complete. 30 FPS sustained. | Add color-filtered beams (red/blue); add a timed challenge mode | 6–8 |
| | | | - Light beam system (raycast + LineRenderer) | | | | | | |
| | | | - Door triggers linked to beam targets | | | | | | |
| | | | - Camera transitions between rooms | | | | | | |
| | | | - Baked lightmaps for atmosphere | | | | | | |
| 5 | **Gravity Garden** | Tend a small floating garden by solving physics puzzles to route water to plants | - Water flow simulation (simple: trigger zones along a path, not fluid sim) | Rotate platforms to change the water's path. Some plants need water in a specific sequence. | Physics-based puzzle design, animation-driven mechanics, simple shader work (water surface), multi-step puzzle chains | Med — animated water shader needs to be kept simple for mobile GPU | 1 garden, 3 plants, water routing puzzle solved, garden blooms. Runs on phone. | Add a day/night cycle (baked lighting swap); add a second garden | 6–8 |
| | | | - Platform rotation (constrained axes) | | | | | | |
| | | | - Animated water (scroll UVs on a plane — no fluid sim) | | | | | | |
| | | | - Sequential puzzle logic | | | | | | |
| | | | - Plant growth animation (scale tween) | | | | | | |
| 6 | **Rune Runner** | Run through a series of corridor rooms, matching rune symbols to open gates and avoid traps | - Pattern matching (observe rune → select correct rune at gate) | Runes are shown briefly on walls; player must remember and input the pattern at gates. Speed increases pressure. | UI pattern input system, basic trap/hazard mechanics (moving obstacles), timer/pressure systems, NavMesh for simple patrol enemies (optional) | Med — moving obstacles need consistent physics frame timing on mobile | 5 corridor rooms, rune patterns work, traps function, completion screen. Stable 30 FPS. | Add a scoring system; add increasingly complex rune patterns | 7–9 |
| | | | - Memory/pattern puzzle (show → recall → input) | | | | | | |
| | | | - Moving obstacles (lerp between points) | | | | | | |
| | | | - Timer pressure system | | | | | | |
| | | | - Health system (3 hits = restart room) | | | | | | |
| 7 | **Sky Isles** | Explore 3 floating islands connected by bridges, solving one puzzle per island to activate a central portal | - Multi-island world (small seamless scene or additive loading) | Each island has a distinct puzzle type: (1) pressure plates + timing, (2) symbol matching, (3) block pushing on a grid. Completing all 3 activates the final portal. | Scene management (additive loading or large scene optimization), combining multiple puzzle types in one game, world design with traversal, save system (per-island progress) | Med-High — multi-area scene needs LOD, occlusion culling; save system complexity | 3 islands, 3 puzzles, portal activates, ending sequence. Saves progress between sessions. < 100 MB APK. | Add hidden collectibles per island; add an NPC guide with dialogue | 8–10 |
| | | | - Pressure plate + timing puzzle | | | | | | |
| | | | - Symbol matching puzzle | | | | | | |
| | | | - Grid-based block pushing | | | | | | |
| | | | - Save/load system (JSON to persistent storage) | | | | | | |

### Projects 8–10: Release Candidates

| # | Project Name | Core Loop | Key Mechanics | Puzzle Hook | What I Learn | Android Risk | MVP "Done" | Stretch Goals | Est. Weeks (2 hrs/wk) |
|---|---|---|---|---|---|---|---|---|---|
| 8 | **The Clockwork Keep** | Explore a multi-floor mechanical tower, repairing gear mechanisms to ascend and escape | - Gear placement puzzles (pick up gears, place in slots, mechanisms activate) | Gears of different sizes must be placed correctly to drive platforms, open doors, and rotate bridges. Wrong placement jams the mechanism. | Complex interconnected puzzle systems, vertical level design, mechanical animation (gear rotation), audio design (satisfying clicks/clanks), polished UI with settings menu | High — many animated objects per floor; gear rotation visuals need batching | 3 floors, gear puzzle per floor, ascend to roof, ending cinematic (simple). Settings menu (volume, quality). 30 FPS. Save works. < 120 MB APK. | Add a 4th bonus floor; add accessibility options | 10–12 |
| | | | - Gear inventory + placement | | | | | | |
| | | | - Mechanical animation chains | | | | | | |
| | | | - Vertical traversal (stairs, lifts) | | | | | | |
| | | | - Settings menu + audio management | | | | | | |
| | | | - Polish: screen shake, haptics, SFX | | | | | | |
| 9 | **Echoes of Stone** | Explore ancient ruins across 4 biome areas, solving environmental puzzles using an "echo" mechanic (replay past events) | - Echo system: activate a stone → watch a ghostly replay of a past event → use the clue to solve the present puzzle | The echo ghosts show you what happened in each area — a bridge that collapsed, a statue that moved, a river that flowed. You must reverse or replicate the event to progress. | Narrative design, ghost/replay systems (record + replay transform data), biome-based level design (forest, desert, water, mountain), cutscene/narrative triggers, Play Store preparation | High — replay system + multiple biomes need careful memory management and LOD | 4 biome areas, echo mechanic works in each, narrative arc with beginning/middle/end, full UI (main menu, pause, settings, credits). < 150 MB APK. Privacy policy page. | Add voice-over narration; add a photo mode | 12–16 |
| | | | - Ghost replay system (record/playback transforms) | | | | | | |
| | | | - 4 biome areas with distinct art (asset kit recolors) | | | | | | |
| | | | - Environmental manipulation (move objects to match echoes) | | | | | | |
| | | | - Narrative system (dialogue + cutscene triggers) | | | | | | |
| | | | - Full UI: main menu, pause, settings, credits | | | | | | |
| 10 | **Lantern & Labyrinth** | Navigate a procedurally-hinted labyrinth using a magic lantern that reveals hidden paths and puzzles | - Lantern mechanic: hold lantern → hidden elements glow/appear (shader-based reveal) | The labyrinth has invisible walls, hidden doors, and illusory floors. The lantern reveals the truth in a radius around the player. Puzzles require toggling the lantern on/off strategically. | Shader programming (reveal/dissolve effect), procedural-assist level design, advanced camera work (tight spaces), full game polish loop (icon, screenshots, store listing), Play Store submission | High — reveal shader + labyrinth rendering need careful optimization; procedural elements must be mobile-safe | Multi-section labyrinth (hand-crafted, not procedural), lantern reveal works, 6+ puzzles, full game flow (menu → play → end → credits), Play Store listing ready. < 150 MB. | Add daily challenge mode; add accessibility features (colorblind, text size) | 14–18 |
| | | | - Shader-based reveal system (stencil or dissolve) | | | | | | |
| | | | - Labyrinth design (modular tile-based) | | | | | | |
| | | | - Hidden element system (invisible walls, illusory floors) | | | | | | |
| | | | - Full game polish (icon, screenshots, store listing) | | | | | | |
| | | | - Play Store submission pipeline | | | | | | |

---

## E) First 8 Weeks Plan (Project 1: Cube Walker)

Each session is exactly 2 hours. Every week ends with something runnable on your Android phone.

### Week 1: Install + Empty Scene on Phone
**Goal:** Verify the entire pipeline works — editor to phone.

| Time | Task |
|---|---|
| 0:00–0:30 | Install Unity Hub + Unity 6 LTS with Android Build Support (may need to pre-download before the session) |
| 0:30–1:00 | Create new 3D (URP) project called "CubeWalker". Switch platform to Android (File → Build Settings → Android). |
| 1:00–1:30 | Set up phone for USB debugging. Connect phone. Hit "Build and Run" on the empty scene. Confirm a blank/skybox screen appears on phone. |
| 1:30–2:00 | Add a Plane (ground) and a Cube (player stand-in) to the scene. Build and Run again. See cube on phone. Initialize Git repo (`git init`, `.gitignore` for Unity — see Section F). |

**Done when:** You see a cube sitting on a plane on your Android phone. Git repo initialized.

---

### Week 2: Character Movement
**Goal:** Move the cube with on-screen touch input.

| Time | Task |
|---|---|
| 0:00–0:20 | Import the Input System package (Window → Package Manager → Input System). Accept the restart prompt. |
| 0:20–1:00 | Create a C# script `PlayerMovement.cs`. Use a virtual joystick or simple touch-drag to move the cube on the XZ plane. Start with `transform.Translate()`. |
| 1:00–1:30 | Add a Rigidbody to the cube. Switch movement to `rb.MovePosition()` for physics-based movement. Adjust speed. |
| 1:30–2:00 | Build and Run. Test touch movement on phone. Tune speed and responsiveness. Git commit. |

**Done when:** Cube moves on the ground via touch input on your phone. No falling through floor.

---

### Week 3: Third-Person Camera
**Goal:** Camera follows the player smoothly.

| Time | Task |
|---|---|
| 0:00–0:20 | Install Cinemachine package. Create a Cinemachine Virtual Camera. |
| 0:20–1:00 | Set the Virtual Camera to "3rd Person Follow" (Body) and "Composer" (Aim). Assign the cube as the Follow and Look At target. Adjust shoulder offset, distance, damping. |
| 1:00–1:30 | Add camera orbit control: swipe on the right half of the screen to rotate the camera. Use Cinemachine's input provider with touch. |
| 1:30–2:00 | Build and Run. Test on phone — does the camera feel good? Tune damping values. Git commit. |

**Done when:** Camera follows the cube in third-person. Touch to orbit works. Playable on phone.

---

### Week 4: Room + Box Push Mechanic
**Goal:** A room exists, and you can push a box.

| Time | Task |
|---|---|
| 0:00–0:30 | Build a simple room using Unity primitives (planes for floor/ceiling, cubes for walls) or import a free room asset from Kenney. Add materials with solid colors. |
| 0:30–1:15 | Add a pushable box: a Cube with Rigidbody (constrain Y rotation, freeze Y position). The player pushes it by walking into it (physics-based). Adjust mass and friction. |
| 1:15–2:00 | Build and Run. Test pushing the box on phone. Make sure it doesn't fly away or clip through walls. Git commit. |

**Done when:** You're in a room. You can push a box by walking into it. Runs on phone.

---

### Week 5: Floor Switch + Door
**Goal:** Push the box onto a switch. Door opens.

| Time | Task |
|---|---|
| 0:00–0:40 | Create a floor switch: a flat colored quad with a Box Collider (Is Trigger). Write a script `FloorSwitch.cs` — when the box enters the trigger, set `activated = true`. |
| 0:40–1:20 | Create a door: a cube that blocks a doorway. Write a script `Door.cs` — listens for the switch activation and moves the door upward (lerp or animation). |
| 1:20–2:00 | Connect them: switch activates → door opens. Test. Build and Run on phone. Git commit. |

**Done when:** Push box onto switch → door opens. Full puzzle loop works on phone.

---

### Week 6: Win Screen + Basic UI
**Goal:** Walk through the door, see a "You Win!" screen. Add a restart button.

| Time | Task |
|---|---|
| 0:00–0:40 | Add a trigger zone behind the door. When the player enters it, load a "WinScreen" scene (or enable a Canvas overlay). Use `SceneManager.LoadScene()`. |
| 0:40–1:20 | Create a simple UI Canvas: "You Win!" text (TextMeshPro) + "Play Again" button. Wire the button to reload the game scene. Size UI elements for touch (min 48dp tap targets). |
| 1:20–2:00 | Build and Run. Full flow: start → push box → door opens → walk through → win screen → restart. Git commit. |

**Done when:** Complete game loop works on phone. You can play start-to-finish and restart.

---

### Week 7: Polish + Visual Pass
**Goal:** Replace programmer art. Add basic SFX. Make it feel like a game.

| Time | Task |
|---|---|
| 0:00–0:40 | Replace the cube player with a free character model (Kenney or KayKit). Add idle/walk animations using an Animator Controller with a simple blend tree or two states. |
| 0:40–1:20 | Add free SFX (footsteps, box scrape, door open, win jingle) from Kenney Audio or freesound.org. Use `AudioSource.PlayOneShot()`. |
| 1:20–2:00 | Add baked lighting (Window → Rendering → Lighting → Generate Lighting). Test on phone — check FPS. Git commit. |

**Done when:** Game has a character model, animations, sound effects, and baked lighting. Still runs at 30+ FPS on phone.

---

### Week 8: Android Performance Pass + Build
**Goal:** Profile, optimize, and produce a release-ready APK.

| Time | Task |
|---|---|
| 0:00–0:40 | Open the Profiler (Window → Analysis → Profiler). Connect to phone via USB. Play for 3+ minutes. Check: CPU frame time < 33ms? GPU < 33ms? Memory < 500 MB? Draw calls < 50? |
| 0:40–1:20 | Fix any issues: enable static batching, compress textures to ASTC, reduce shadow distance or disable shadows, strip unused shaders in Project Settings → Graphics. |
| 1:20–1:50 | Build a signed APK/AAB: Player Settings → Publishing Settings → create a keystore. Build an AAB (Android App Bundle) for Play Store compatibility. Test the signed build on phone. |
| 1:50–2:00 | Final Git commit + tag: `git tag v1.0-cubewalker`. |

**Done when:** Signed AAB runs on phone. Performance is stable at 30 FPS over 5+ minutes. Ready for Play Store if desired. Project 1 is COMPLETE.

---

## F) Tooling & Workflow

### Version Control

**Use Git + GitHub (free).**

- Initialize at project creation: `git init`
- Use Unity's official `.gitignore`: [github.com/github/gitignore/blob/main/Unity.gitignore](https://github.com/github/gitignore/blob/main/Unity.gitignore)
- Set Asset Serialization to "Force Text" (Edit → Project Settings → Editor → Asset Serialization → Force Text) — this makes Unity files diff-able
- Commit after every session (2 hrs = 1 commit minimum)
- Push to GitHub for backup. Free private repos are fine.

**Minimal folder structure:**
```
Assets/
├── _Project/          ← All your custom content here
│   ├── Scripts/
│   ├── Prefabs/
│   ├── Scenes/
│   ├── Materials/
│   ├── Audio/
│   ├── UI/
│   └── Animations/
├── ThirdParty/        ← Imported free assets (Kenney, KayKit, etc.)
├── Plugins/           ← Any native plugins (rare for beginners)
└── Settings/          ← URP settings, quality settings
```

Prefix your project folder with `_` so it sorts to the top in the Unity editor.

### Free Asset Sourcing Strategy

| Source | What It Offers | License | Caution |
|---|---|---|---|
| [Kenney.nl](https://kenney.nl/assets) | 40K+ assets (3D, 2D, audio, UI). Clean stylized look. | CC0 (public domain) — no attribution required | None. Safest option. |
| [KayKit (itch.io)](https://kaylousberg.itch.io/) | Stylized 3D character packs, environment kits | CC0 | None. Excellent quality. |
| [Quaternius](https://quaternius.com/) | Low-poly 3D packs (nature, characters, buildings) | CC0 | None. Great for environments. |
| [itch.io CC0 tag](https://itch.io/game-assets/assets-cc0) | Huge variety of CC0 assets | CC0 (verify per-asset) | **Always verify license on each page.** Some creators change terms. |
| [Polyhaven](https://polyhaven.com/) | HDRIs, PBR textures, some 3D models | CC0 | Textures may need resizing for mobile. |
| [ambientCG](https://ambientcg.com/) | 1,500+ PBR materials | CC0 | Same as Polyhaven — resize for mobile. |
| [OpenGameArt.org](https://opengameart.org/) | Mixed 2D/3D/audio assets | Varies (CC0, CC-BY, GPL) | **Check each asset's license.** Some require attribution (CC-BY) or are copyleft (GPL). Do not assume CC0. |
| [Unity Asset Store (free section)](https://assetstore.unity.com/?free=true) | Unity-ready packages | Unity Asset Store EULA | Free assets are licensed for use in Unity projects only. Check each listing for restrictions. |
| [Fab (formerly UE Marketplace + Sketchfab)](https://www.fab.com/) | Quixel Megascans (free with UE), other free packs | Epic Content License | **Megascans are free only for Unreal Engine projects.** For Unity, check individual asset licenses. |

**Licensing rules of thumb:**
- CC0 = do anything, no attribution, commercial OK
- CC-BY = must credit the creator (add to your credits screen)
- CC-BY-SA = must credit AND share your derivative work under the same license (risky for commercial games — avoid unless you understand the implications)
- GPL = copyleft; may require open-sourcing your game code (avoid for commercial releases)
- **When in doubt, skip the asset.** There are enough CC0 options.

### Testing Strategy on Mid-Range Android

**Profiling cadence:**
- **Every session (weekly):** Build to phone. Play for 2+ minutes. Watch for stutters, freezes, or heat.
- **Every 3 sessions:** Open Unity Profiler connected to phone. Record 2 minutes of gameplay. Check the metrics below.
- **Before any "release" milestone:** Run a 10-minute sustained play test. Monitor FPS, battery drain, and phone temperature.

**Metrics to watch:**

| Metric | Tool | Target | Red Flag |
|---|---|---|---|
| Frame time | Unity Profiler → CPU/GPU | < 33ms per frame (30 FPS) | > 50ms spikes, sustained > 40ms |
| Draw calls | Frame Debugger, Profiler → Rendering | < 100 | > 150 consistently |
| SetPass calls | Profiler → Rendering | < 50 | > 80 |
| Texture memory | Memory Profiler | < 150 MB | > 300 MB |
| Total RAM | Memory Profiler | < 800 MB | > 1.2 GB |
| GC allocations | Profiler → CPU → GC Alloc | < 1 KB per frame | Any per-frame allocation in Update() |
| APK size | Build output | < 150 MB | > 150 MB (Play Store limit for base APK) |
| Battery drain | Manual observation | < 15% per 30 min | > 25% per 30 min |
| Device temperature | Touch the phone | Warm, not hot | Too hot to hold comfortably |

---

## G) Self-Audit Checklist

### Shippability Checks (Yes/No for Each)

| # | Check | Details |
|---|---|---|
| 1 | Does the game launch without crashing on my target phone? | Cold start — install from APK/AAB, launch, play through. |
| 2 | Can a new player complete the game without external instructions? | Hand it to a friend. Watch silently. Do they finish? |
| 3 | Is the framerate stable at 30+ FPS for 10 consecutive minutes? | Use Profiler or FPS counter overlay. No drops below 25. |
| 4 | Does the game handle interruptions (phone call, home button, lock screen)? | `OnApplicationPause` / `OnApplicationFocus` — does it resume correctly? |
| 5 | Are all assets legally cleared for commercial use? | Audit every imported asset. CC0 or Asset Store EULA confirmed? |
| 6 | Is the APK/AAB under 150 MB? | Check build output size. |
| 7 | Does the game target Android API 34+? | Required by Google Play since August 2024. Check Player Settings. |
| 8 | Is there a privacy policy? | Required by Google Play even if you collect no data. Use a free generator. Host on a simple webpage. |
| 9 | Does the UI scale correctly on different screen sizes/aspect ratios? | Test on at least 2 devices or use Unity's Device Simulator. |
| 10 | Is the save system working? | Close the app mid-game. Reopen. Is progress saved? |
| 11 | Are there no placeholder or debug elements in the build? | No "TODO" text, debug logs enabled, or test buttons visible. |
| 12 | Have I tested with airplane mode on? | The game should work fully offline unless it's designed otherwise. |

### Top 5 Risks + Mitigations

| # | Risk | Why It's Dangerous | Mitigation |
|---|---|---|---|
| 1 | **Motivation decay** | At 2 hrs/week, projects stretch over months. Excitement fades. Weeks get skipped. | Keep projects TINY. Ship something every 4–6 weeks. Seeing a finished game on your phone is the best motivator. Never start Project N+1 before finishing Project N. |
| 2 | **Scope creep** | "Just one more feature" turns a 4-week project into a 6-month one. | Define MVP before starting (see project table). Write it down. If a feature isn't on the MVP list, it goes in "stretch goals" and is not attempted until MVP ships. |
| 3 | **Asset mismatch** | Mixing assets from different packs (realistic trees + cartoon characters) looks terrible and breaks visual cohesion. | Pick ONE asset pack family per project (e.g., all Kenney or all KayKit). Recolor/resize within the same pack rather than mixing packs. |
| 4 | **Performance surprise at the end** | Building and testing only on PC, then finding the game runs at 12 FPS on phone. | Build to phone EVERY session (weekly). Profile every 3 sessions. This is non-negotiable. Never develop more than 2 weeks without an on-device test. |
| 5 | **Play Store submission complexity** | First-time submission involves: developer account ($25), app signing, content rating questionnaire, privacy policy, store listing (screenshots, description, icon), and review wait time (hours to days). | Treat Play Store submission as its own dedicated 2–4 hour task. Do NOT try to "figure it out at the end." Follow Google's official pre-launch checklist step by step. Do a test submission with your first tiny game to learn the process. |

---

## Sources

- [Unity Plans & Pricing](https://unity.com/products)
- [Unity Pricing Updates FAQ](https://unity.com/pricing-updates)
- [Unity 6 Releases & Support](https://unity.com/releases/unity-6/support)
- [Unity 6 Download](https://unity.com/releases/unity-6)
- [Unity Android Environment Setup Docs](https://docs.unity3d.com/6000.3/Documentation/Manual/android-sdksetup.html)
- [Godot Engine Download Archive — 4.5.1 Stable](https://godotengine.org/download/archive/4.5.1-stable/)
- [Godot Android Export Docs](https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_android.html)
- [Godot 4.6 Dev5 — Android Gradle Improvements](https://digitalproduction.com/2025/12/04/godot-4-6-dev5-lands-d3d12-default-delta-patching-android-gradle-2d-boosts/)
- [Unreal Engine Licensing](https://www.unrealengine.com/en-US/license)
- [Unreal Engine Android Support Docs](https://dev.epicgames.com/documentation/en-us/unreal-engine/android-support-for-unreal-engine)
- [Unreal Engine Royalty Reporting Update](https://www.unrealengine.com/en-US/news/unreal-engines-improved-royalty-reporting-system)
- [Defold License](https://defold.com/license/)
- [Defold 2025 Retrospective](https://defold.com/2026/01/02/Defold-2025-Retrospective/)
- [Kenney Assets](https://kenney.nl/assets)
- [itch.io CC0 Game Assets](https://itch.io/game-assets/assets-cc0)
- [Polyhaven](https://polyhaven.com/)
- [ambientCG](https://ambientcg.com/)
- [OpenGameArt.org](https://opengameart.org/)
