const { MongoClient } = require('mongodb');
const url = 'mongodb://localhost:27017/';

export async function insertScoretb(collection, myobj) {
  const result = await collection.insertOne(myobj);
  console.log('Document inserted:', result.insertedId);
}

export async function findschooltb(collection, username) {
  const user = await collection.findOne({ name: username });
  return user;
}

async function main() {
  const client = new MongoClient(url, { useNewUrlParser: true, useUnifiedTopology: true });

  try {
    await client.connect();
    const database = client.db('local');
    const collection = database.collection('score');
  } finally {
    await client.close();
    console.log('Connection closed');
  }
}

main().catch((err) => console.error(err));