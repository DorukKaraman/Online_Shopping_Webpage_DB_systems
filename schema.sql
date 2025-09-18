-- ================================
-- Online Auction System Schema
-- ================================

DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Seller;
DROP TABLE IF EXISTS Buyer;
DROP TABLE IF EXISTS Category;
DROP TABLE IF EXISTS auction_categorizes;
DROP TABLE IF EXISTS owns;
DROP TABLE IF EXISTS TakesBids;
DROP TABLE IF EXISTS bill_Generates_Payday;

-- --------------------
-- User Table
-- --------------------
CREATE TABLE User (
    ssn TEXT PRIMARY KEY,
    firstName TEXT NOT NULL,
    lastName TEXT NOT NULL,
    password TEXT NOT NULL
);

-- --------------------
-- Seller Table
-- --------------------
CREATE TABLE Seller (
    SellerID TEXT PRIMARY KEY,
    IBAN TEXT,
    FOREIGN KEY (SellerID) REFERENCES User(ssn)
);

-- --------------------
-- Buyer Table
-- --------------------
CREATE TABLE Buyer (
    BuyerID TEXT PRIMARY KEY,
    FOREIGN KEY (BuyerID) REFERENCES User(ssn)
);

-- --------------------
-- Category Table
-- --------------------
CREATE TABLE Category (
    categoryName TEXT PRIMARY KEY
);

-- --------------------
-- Auction Table
-- --------------------
CREATE TABLE auction_categorizes (
    startPrice INTEGER NOT NULL,
    description TEXT NOT NULL,
    title TEXT NOT NULL,
    categoryName TEXT NOT NULL,
    currentPrice INTEGER NOT NULL,
    status TEXT NOT NULL,               -- OnGoing or Ended
    endDate TEXT NOT NULL,              -- stored as dd-mm-yyyy string
    startDate TEXT NOT NULL,            -- stored as yyyy-mm-dd
    finalBidID TEXT,
    auctionNo INTEGER PRIMARY KEY,
    buyItPrice INTEGER NOT NULL,
    FOREIGN KEY (categoryName) REFERENCES Category(categoryName)
);

-- --------------------
-- Ownership (Seller -> Auction)
-- --------------------
CREATE TABLE owns (
    auctionNo INTEGER,
    SellerID TEXT,
    PRIMARY KEY (auctionNo, SellerID),
    FOREIGN KEY (auctionNo) REFERENCES auction_categorizes(auctionNo),
    FOREIGN KEY (SellerID) REFERENCES Seller(SellerID)
);

-- --------------------
-- Bids (Buyer -> Auction)
-- --------------------
CREATE TABLE TakesBids (
    buyerSsn TEXT,
    auctionNo INTEGER,
    biddingPrice INTEGER NOT NULL,
    PRIMARY KEY (buyerSsn, auctionNo),
    FOREIGN KEY (buyerSsn) REFERENCES Buyer(BuyerID),
    FOREIGN KEY (auctionNo) REFERENCES auction_categorizes(auctionNo)
);

-- --------------------
-- Bills (Generated after auction ends)
-- --------------------
CREATE TABLE bill_Generates_Payday (
    tranNo INTEGER PRIMARY KEY AUTOINCREMENT,
    auctionNo INTEGER NOT NULL,
    finalBidID TEXT NOT NULL,
    netAmount INTEGER NOT NULL,
    SellerID TEXT NOT NULL,
    FOREIGN KEY (auctionNo) REFERENCES auction_categorizes(auctionNo),
    FOREIGN KEY (finalBidID) REFERENCES Buyer(BuyerID),
    FOREIGN KEY (SellerID) REFERENCES Seller(SellerID)
);
