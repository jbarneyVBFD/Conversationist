//
//  AppDelegate.swift
//  Conversationist
//
//  Created by John Barney on 6/9/24.
//

import Foundation
import UIKit
import AWSCore
import AWSCognitoIdentityProvider


class AppDelegate: UIResponder, UIApplicationDelegate {
    var window: UIWindow?

    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        let credentialsProvider = AWSCognitoCredentialsProvider(regionType: .USEast1, identityPoolId: "us-east-1:46a48c96-1bfa-44b0-a22e-d2164d0b1030")
        let configuration = AWSServiceConfiguration(region: .USEast1, credentialsProvider: credentialsProvider)
        AWSServiceManager.default().defaultServiceConfiguration = configuration
        
        // Configure user pool
        let serviceConfiguration = AWSServiceConfiguration(region: .USEast1, credentialsProvider: nil)
        let userPoolConfiguration = AWSCognitoIdentityUserPoolConfiguration(clientId: "7e9j1avqgksoj7qrn4842nm7d9", clientSecret: nil, poolId: "us-east-1_ZGFM9OT8K")
        AWSCognitoIdentityUserPool.register(with: serviceConfiguration, userPoolConfiguration: userPoolConfiguration, forKey: "UserPool")
        
        return true
    }
}

