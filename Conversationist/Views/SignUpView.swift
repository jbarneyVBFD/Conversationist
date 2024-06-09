//
//  SignUpView.swift
//  Conversationist
//
//  Created by John Barney on 6/9/24.
//

import SwiftUI

struct SignUpView: View {
    @State private var password: String = ""
    @State private var email: String = ""
    @State private var message: String = ""
    var body: some View {
        VStack{
            TextField("Email", text: $email)
                .textFieldStyle(.roundedBorder)
                .padding()
        }
    }
}

#Preview {
    SignUpView()
}
