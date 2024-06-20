//
//  ContentView.swift
//  Conversationist
//
//  Created by John Barney on 6/7/24.
//

import SwiftUI

struct ContentView: View {
    @StateObject var storeManager: StoreManager = StoreManager()
    var body: some View {
        NavigationView {
            VStack {
                Image(systemName: "globe")
                    .imageScale(.large)
                    .foregroundStyle(.tint)
                Text("Hello, world!")
            }
        }
        .environmentObject(storeManager)
        .padding()
    }
}

#Preview {
    ContentView()
}
