//
//  StoreManager.swift
//  Conversationist
//
//  Created by John Barney on 6/18/24.
//
//  The Store is responsible for requesting products from the App Store and starting purchases; other parts of
//  the app query the store to learn what products have been purchased.
//

import Foundation
import StoreKit

typealias Transaction = StoreKit.Transaction
typealias RenewalInfo = StoreKit.Product.SubscriptionInfo.RenewalInfo
typealias RenewalState = StoreKit.Product.SubscriptionInfo.RenewalState

public enum StoreError: Error {
    case failedVerification
}

class StoreManager: ObservableObject {
    
    @Published private(set) var subscriptions: [Product]
    var updateListenerTask: Task<Void, Error>? = nil
    
    init() {

        //Start a transaction listener as close to app launch as possible so you don't miss any transactions.
        updateListenerTask = listenForTransactions()

        Task {
            //Initialize the store by starting a product request.
            await requestProducts()
        }
    }

    deinit {
        updateListenerTask?.cancel()
    }
    
    func listenForTransactions() -> Task<Void, Error> {
        return Task.detached {
            //Iterate through any transactions which didn't come from a direct call to `purchase()`.
            for await result in Transaction.updates {
                do {
                    let transaction = try self.checkVerified(result)

                    //Deliver content to the user.
                    await self.updatePurchasedIdentifiers(transaction)

                    //Always finish a transaction.
                    await transaction.finish()
                } catch {
                    //StoreKit has a receipt it can read but it failed verification. Don't deliver content to the user.
                    print("Transaction failed verification")
                }
            }
        }
    }
    
    @MainActor
    func requestProducts() async {
        do {
            //Request products from the App Store using the identifiers defined in the Products.plist file.
            subscriptions = try await Product.products(for: ["Conversationist.monthly", "Conversationist.yearly"])

        } catch {
            print("Failed product request: \(error)")
        }
    }
    
    func purchase(_ product: Product) async throws -> Transaction? {
        //Begin a purchase.
        let result = try await product.purchase()

        switch result {
        case .success(let verification):
            let transaction = try checkVerified(verification)

            //Deliver content to the user.
            await updatePurchasedIdentifiers(transaction)

            //Always finish a transaction.
            await transaction.finish()

            return transaction
        case .userCancelled, .pending:
            return nil
        default:
            return nil
        }
    }
}
