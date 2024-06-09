//
//  ConversationistApp.swift
//  Conversationist
//
//  Created by John Barney on 6/7/24.
//

import SwiftUI

@main
struct ConversationistApp: App {
    // Create the AppDelegate
    @UIApplicationDelegateAdaptor(AppDelegate.self) var appDelegate
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
