//
//  SignUpView.swift
//  Conversationist
//
//  Created by John Barney on 6/9/24.
//

import SwiftUI
import AWSCognitoIdentityProvider

struct SignUpView: View {
    @State private var password: String = ""
    @State private var email: String = ""
    @State private var message: String = ""
    var body: some View {
        VStack{
            TextField("Email", text: $email)
                .textFieldStyle(.roundedBorder)
                .padding()
            TextField("Password", text: $password)
                .textFieldStyle(.roundedBorder)
                .padding()
            Button("Sign Up") {
                signUp()
            }
        }
    }
    
    func signUp() {
        guard let pool = AWSCognitoIdentityUserPool(forKey: "UserPool") else {
            message = "User pool not configured."
            return
        }
            
        let userAttributes = [
            AWSCognitoIdentityUserAttributeType(name: "email", value: email)
        ]
            
        pool.signUp(email, password: password, userAttributes: userAttributes, validationData: nil).continueWith { task in
            DispatchQueue.main.async {
                if let error = task.error as NSError? {
                    message = "Error: \(error.userInfo["message"] as? String ?? "Unknown error")"
                } else {
                    message = "Sign-up successful"
                }
            }
            return nil
        }
    }
}

#Preview {
    SignUpView()
}
