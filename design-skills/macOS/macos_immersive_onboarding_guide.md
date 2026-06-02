# macOS Immersive Onboarding Skill Guide

**Title:** Building Delightful, "Crazy Effects" First-Launch & Setup Experiences for macOS Apps (Agnostic / Perplexity Arc Style)

**Goal:** Create premium, immersive onboarding that feels like Perplexity Personal Computer (guided permissions, connectors, deep integration flows) or Arc Browser (playful orb/intro animations, smooth reveals, blur/vibrancy). This is for the **post-DMG first-launch wizard** inside your SwiftUI + AppKit macOS app.

**Target Feel:**
- Whole-screen or large immersive views with dynamic blur/frosted glass reacting to desktop.
- Fluid movements, growth animations, staggered text, particle/orb-like reveals.
- Subtle sounds on state changes.
- Guided multi-step wizard for sign-in → permissions → integrations.
- High delight on first open, skippable for returning users.

**Compatibility:** macOS 15 Sequoia+ (SwiftUI 5+/6+), Xcode 16+ recommended.

---

## 1. Prerequisites & Project Setup

1. Create new macOS App in Xcode → SwiftUI + AppKit interop.
2. Enable necessary capabilities in Signing & Capabilities:
   - App Sandbox (if needed, configure for full disk etc.)
   - Hardened Runtime
   - For deep integrations (Perplexity-like): Accessibility, Screen Recording, Full Disk Access entitlements (request at runtime).
3. Add packages:
   - `AnimateText` or similar for staggered text (or build custom).
   - AVFoundation for video/audio.
4. Info.plist: Set `Application is agent (UIElement)` = NO for standard apps.

**Key Files to Create:**
- `OnboardingManager.swift` (state, first launch check)
- `ImmersiveOnboardingView.swift`
- `PermissionStepView.swift`, `StepView.swift`
- Custom `NSWindow` helpers.

---

## 2. Detecting First Launch & Presenting Onboarding

```swift
import SwiftUI

@main
struct MyApp: App {
    @AppStorage("hasCompletedOnboarding") private var hasCompletedOnboarding = false
    @State private var showOnboarding = false

    var body: some Scene {
        WindowGroup {
            ContentView()
                .onAppear {
                    if !hasCompletedOnboarding {
                        showOnboarding = true
                    }
                }
                .fullScreenCover(isPresented: $showOnboarding) {
                    ImmersiveOnboardingView {
                        hasCompletedOnboarding = true
                        showOnboarding = false
                    }
                }
        }
        // Add custom Window scenes for floating elements if needed
    }
}
```

Alternative: Use `openWindow` for dedicated onboarding window ID.

---

## 3. Immersive Window Setup (The "Whole Screen" Magic)

Use **AppKit** for precise control over floating/borderless windows + SwiftUI hosting.

### Background Dim Overlay (Arc-style desktop fade)
```swift
func createBackgroundOverlay() -> NSWindow {
    let screen = NSScreen.main!.frame
    let window = NSWindow(contentRect: screen,
                          styleMask: [.borderless],
                          backing: .buffered,
                          defer: false)
    window.alphaValue = 0
    window.backgroundColor = .black.withAlphaComponent(0.85)
    window.level = .floating
    window.ignoresMouseEvents = true
    window.isOpaque = false
    
    NSAnimationContext.runAnimationGroup { ctx in
        ctx.duration = 0.8
        window.animator().alphaValue = 0.9
    }
    window.makeKeyAndOrderFront(nil)
    return window
}
```

### Main Onboarding Window (Borderless/Transparent)
```swift
let onboardingWindow = NSWindow(contentRect: NSRect(x: 0, y: 0, width: 900, height: 620),
                                styleMask: [.fullSizeContentView, .borderless],
                                backing: .buffered,
                                defer: false)
onboardingWindow.titlebarAppearsTransparent = true
onboardingWindow.isOpaque = false
onboardingWindow.backgroundColor = .clear
onboardingWindow.hasShadow = true
onboardingWindow.level = .floating
onboardingWindow.contentView = NSHostingView(rootView: OnboardingContentView(onComplete: { ... }))
```

Set `ignoresSafeArea(.all)` in SwiftUI root.

For true full-screen immersive: `.fullScreenCover` or custom `ImmersiveSpace` (visionOS influence but adaptable).

---

## 4. Blur & Vibrancy Effects

- **SwiftUI Simple:** 
  ```swift
  ZStack {
      Rectangle()
          .background(.ultraThinMaterial)  // or .regularMaterial, .thickMaterial, .ultraThickMaterial
          .ignoresSafeArea()
      // Foreground content with blur radius animations
  }
  .background(.regularMaterial) // On parent
  ```

- **Advanced AppKit:** Wrap `NSVisualEffectView`
  ```swift
  struct VisualEffectView: NSViewRepresentable {
      var material: NSVisualEffectView.Material = .hudWindow
      var blendingMode: NSVisualEffectView.BlendingMode = .behindWindow
      
      func makeNSView(context: Context) -> NSVisualEffectView {
          let view = NSVisualEffectView()
          view.material = material  // .fullScreenUI, .popover etc.
          view.blendingMode = blendingMode
          view.state = .active
          return view
      }
      // ...
  }
  ```

Combine: Background video/gradient + material overlay + animated foreground.

---

## 5. Animations & Movements (The "Crazy" Part)

**Core Modifiers:**
- `withAnimation(.spring(response: 0.5, dampingFraction: 0.7, blendDuration: 0.3))`
- `.transition(.scale.combined(with: .opacity).combined(with: .offset))`
- Keyframe animations (WWDC23+): `KeyframeAnimator`
- Matched Geometry for element transitions between steps.

**Orb / Reveal Example (from Arc Recreation):**
- Prepare transparent .mov with FFmpeg: `ffmpeg -framerate 60 -i %03d.png -c:v prores_ks -profile:v 5 -pix_fmt yuva444p10le orb.mov`
- Play with `VideoPlayer(player: AVPlayer(url: ...))`
- On finish (`AVPlayerItemDidPlayToEndTime` notification): 
  - Animate window opacity/background
  - Switch to looping gradient video
  - Reveal UI elements

**Staggered Text:**
Use custom `ATTextAnimateEffect` or manual:
```swift
ForEach(Array(text.enumerated()), id: \.offset) { index, char in
    Text(String(char))
        .opacity(animProgress)
        .blur(radius: 8 * (1 - animProgress))
        .rotation3DEffect(.degrees(15 * (1 - animProgress)), axis: (0,0,1))
        .animation(.spring().delay(Double(index) * 0.025), value: animProgress)
}
```

**State-Driven Steps:**
```swift
@State private var currentStep = 0
@State private var animTrigger = false

ZStack {
    if currentStep == 0 { WelcomeStep() }
    // ...
}
.onChange(of: currentStep) { 
    withAnimation(.easeOut(duration: 0.6)) { animTrigger.toggle() }
}
```

---

## 6. Audio Feedback

```swift
import AVFoundation

func playSuccessSound() {
    NSSound(named: "Glass")?.play()
    // Or custom:
    let player = try? AVAudioPlayer(contentsOf: soundURL)
    player?.play()
}

// Trigger: .onChange(of: permissionGranted) { if $0 { playSuccessSound(); withAnimation... } }
```

Voiceover: Use `AVSpeechSynthesizer` for guided narration.

---

## 7. Multi-Step Wizard Architecture

```swift
enum OnboardingStep: CaseIterable, Identifiable {
    case welcome, signIn, permissions, connectors, complete
    var id: Self { self }
    var title: String { ... }
}

struct ImmersiveOnboardingView: View {
    @State private var currentStep: OnboardingStep = .welcome
    let onComplete: () -> Void
    
    var body: some View {
        ZStack {
            // Background blur + animated gradient/video
            VisualEffectBackground()
            
            VStack {
                ProgressIndicator(current: currentStep)
                
                TabView(selection: $currentStep) {
                    ForEach(OnboardingStep.allCases) { step in
                        StepContent(for: step)
                            .tag(step)
                    }
                }
                .tabViewStyle(.page(indexDisplayMode: .never))
                
                NavigationButtons(currentStep: $currentStep, onComplete: onComplete)
            }
            .padding()
            .frame(maxWidth: 800)
        }
        .onAppear { animateEntry() }
    }
}
```

Include skip button, progress dots with animated highlights.

---

## 8. Permissions & Deep Integration Flows (Perplexity-style)

- Custom explanatory cards with icons, benefits, animated checkmarks.
- Button "Grant in System Settings" → `NSWorkspace.shared.open(URL(string: "x-apple.systempreferences:")!)`
- Poll status with `onReceive` timer or NotificationCenter.
- Success state: Confetti/scale animation + sound + "Next" unlock.

Example cards for:
- Accessibility (for control)
- Screen & System Audio Recording
- Full Disk Access
- Folder/app connectors (use `NSOpenPanel` wrapped nicely)
- Phone pairing / 2FA

Use `@Environment(\.requestAuthorization)` patterns or custom wrappers.

---

## 9. DMG Download Experience Polish

While lighter:
- Beautiful landing page on arc.net/perplexity.ai with step graphics (1. Download, 2. Drag, 3. Launch).
- Custom background, QR for mobile companion.
- Signed/notarized .app in DMG with instructions overlay.

Implement via web, but app can detect "just installed" via file timestamp or UserDefaults.

---

## 10. Best Practices & Advanced Polish

- **Performance:** Preload assets; use `TimelineView` for smooth loops.
- **Accessibility:** VoiceOver labels, reduce motion support (`UIAccessibility.isReduceMotionEnabled`).
- **Testing:** Different screen sizes, light/dark, first vs repeat launch.
- **A/B Delight:** Random subtle variations or user preference.
- **Cleanup:** Fade out overlay windows on dismiss; mark complete only after success.
- **Frameworks:** Combine with Rive/ Lottie for complex illustrations (export to SwiftUI compatible).

**Edge Cases:**
- User quits mid-onboarding → Resume on next launch.
- Permission denied → Helpful recovery screen with "Why we need this" + retry.
- macOS version checks for API availability.

---

## 11. Full Example Code Scaffolds & Resources

**Key Resources:**
- Arc Recreation: https://www.georgecartridge.com/dev-notes/recreate-arc-dia-onboarding-intro (detailed window, FFmpeg, staggered text)
- Kavsoft YouTube: "macOS Onboarding Animation", "Permissions OnBoarding", "Xcode Onboarding" (Patreon source code)
- Apple WWDC: "Explore SwiftUI animation" (10156), "Advanced Animations" (10157)
- SwiftUI Materials docs, NSVisualEffectView
- GitHub gists for borderless windows, full screen overlays.
- YouTube searches: "SwiftUI macOS onboarding blur animation"

**Additional Images/Visual Inspiration:** Search for "macOS SwiftUI onboarding blur" – expect card UIs, gradient backgrounds, animated illustrations.

Implement iteratively: Start with basic steps + blur, add animations, then video/sound, finally permissions.

**Pro Tip for Coding Agents:** Prompt them with specific sections (e.g., "Implement the orb reveal window using the Arc recreation techniques above"). Test in Xcode previews/simulator first, then real device.

---

**Version:** 1.0 | Compiled from Perplexity/Arc analysis + real implementations.
**Usage:** Copy this .md to your repo/wiki. Feed sections to Cursor/Claude/Code agents for modular implementation.

This guide is self-contained and actionable for recreating the premium "wow" effect in any new macOS app.
