const { MongoClient } = require('mongodb');
const url = 'mongodb://localhost:27017/';

export async function insertusertb(collection, myobj) {
  const result = await collection.insertOne(myobj);
  console.log('Document inserted:', result.insertedId);
}

export async function findUsertb(collection, username) {
  const user = await collection.findOne({ name: username });
  return user;
}

async function main() {
  const client = new MongoClient(url, { useNewUrlParser: true, useUnifiedTopology: true });

  try {
    await client.connect();
    console.log('Connected to the database');

    const database = client.db('local');
    const collection = database.collection('userinfo');
  } finally {
    await client.close();
    console.log('Connection closed');
  }
}

main().catch((err) => console.error(err));