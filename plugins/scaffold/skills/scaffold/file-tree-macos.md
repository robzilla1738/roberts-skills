# macOS file tree and conventions

> Phase 3 / 7 reference. Back to [SKILL.md](SKILL.md).

---

## Canonical tree (windowed app)

```text
MyMacApp/
├── MyMacApp.xcodeproj
├── Config/
│   ├── Debug.xcconfig
│   ├── Release.xcconfig
│   ├── Secrets.example.xcconfig
│   └── Secrets.xcconfig          # gitignored
├── MyMacApp/
│   ├── MyMacAppApp.swift         # @main — scenes, commands, service bootstrap
│   ├── App/
│   │   ├── AppModel.swift
│   │   └── AppError.swift
│   ├── Config/
│   │   └── AppConfig.swift
│   ├── Features/
│   │   ├── Main/
│   │   │   ├── MainWindowView.swift
│   │   │   ├── SidebarView.swift
│   │   │   └── DetailPlaceholderView.swift
│   │   ├── Settings/
│   │   │   ├── SettingsRootView.swift
│   │   │   ├── GeneralSettingsView.swift
│   │   │   └── IntegrationsStatusView.swift
│   │   └── Upgrade/
│   │       └── UpgradePlaceholderView.swift
│   ├── Services/
│   │   ├── RevenueCatService.swift
│   │   ├── SparkleUpdaterController.swift
│   │   ├── SentryService.swift
│   │   ├── PostHogService.swift
│   │   ├── AppleSignInService.swift
│   │   ├── APIClient.swift
│   │   └── KeychainStore.swift
│   ├── Models/
│   │   └── Item.swift            # SwiftData @Model
│   └── Resources/
│       ├── Assets.xcassets
│       ├── MyMacApp.entitlements
│       └── Info.plist
├── MyMacAppTests/
├── .gitignore
└── README.md
```

## Menu bar variant

Replace `Features/Main/` with `Features/MenuBar/` + `Features/UtilityWindow/`; add `UtilityModel.swift`.

## Document variant

Add `Features/Document/`, `MyDocument.swift`, use `DocumentGroup` in `MyMacAppApp.swift`.

---

## `.gitignore` (commit this)

```gitignore
# Xcode
build/
DerivedData/
*.xcuserstate
xcuserdata/
*.xccheckout
*.moved-aside
*.hmap
*.ipa
*.dSYM.zip
*.dSYM

# SwiftPM
.build/
.swiftpm/

# Secrets
Config/Secrets.xcconfig
.env.local

# macOS
.DS_Store

# Test results
TestResults.xcresult/
```

---

## Naming conventions

| Item | Convention |
|------|------------|
| App struct | `{{Name}}App` |
| `@main` file | `{{Name}}App.swift` |
| Services | `*Service.swift` or `*Controller.swift` (Sparkle) |
| Views | `*View.swift` |
| SwiftData models | singular noun `@Model` class |
| Bundle ID | `com.company.product` from intake |

---

## Build configurations

| Config | xcconfig | Use |
|--------|----------|-----|
| Debug | `Config/Debug.xcconfig` | Local dev, optional dev API |
| Release | `Config/Release.xcconfig` | Archive, notarization |

Optional: `DIRECT_DISTRIBUTION` Swift flag in Release for direct builds with Sparkle vs MAS.

---

## README sections (required)

1. Scaffold profile + app style
2. Confirmed add-ons + xcconfig keys
3. Distribution + entitlements summary
4. Build/test commands
5. [production-habits-native.md](production-habits-native.md) checklist
