"""
Migration script to rename 'metadata' column to 'message_metadata' in chat_messages table
to resolve SQLAlchemy reserved keyword conflict.

Run this script if you have an existing database with data in the chat_messages table.
If you're starting fresh, you can ignore this script as the new schema will be created correctly.
"""

import os
import sys
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import SQLAlchemyError

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings


def migrate_metadata_column():
    """
    Migrate the 'metadata' column to 'message_metadata' in chat_messages table
    """
    try:
        # Create database engine
        engine = create_engine(settings.DATABASE_URL)
        
        # Check if the table exists and has the old column
        inspector = inspect(engine)
        
        if 'chat_messages' not in inspector.get_table_names():
            print("✓ chat_messages table doesn't exist yet. No migration needed.")
            return True
            
        columns = [col['name'] for col in inspector.get_columns('chat_messages')]
        
        if 'metadata' not in columns:
            if 'message_metadata' in columns:
                print("✓ Migration already completed. The message_metadata column exists.")
                return True
            else:
                print("✓ Neither 'metadata' nor 'message_metadata' columns found. Schema will be created fresh.")
                return True
        
        print("🔄 Starting migration: renaming 'metadata' column to 'message_metadata'...")
        
        with engine.connect() as conn:
            # Start a transaction
            trans = conn.begin()
            
            try:
                # Check database type to use appropriate syntax
                db_dialect = engine.dialect.name
                
                if db_dialect == 'postgresql':
                    # PostgreSQL syntax
                    conn.execute(text(
                        "ALTER TABLE chat_messages RENAME COLUMN metadata TO message_metadata"
                    ))
                elif db_dialect == 'sqlite':
                    # SQLite doesn't support RENAME COLUMN directly, so we need to recreate the table
                    print("🔄 SQLite detected. Creating new table structure...")
                    
                    # Create new table with correct schema
                    conn.execute(text("""
                        CREATE TABLE chat_messages_new (
                            id TEXT PRIMARY KEY,
                            consultation_id TEXT NOT NULL,
                            sender_type TEXT NOT NULL,
                            message_content TEXT NOT NULL,
                            message_metadata TEXT,
                            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (consultation_id) REFERENCES consultations (id)
                        )
                    """))
                    
                    # Copy data from old table to new table
                    conn.execute(text("""
                        INSERT INTO chat_messages_new 
                        (id, consultation_id, sender_type, message_content, message_metadata, timestamp)
                        SELECT id, consultation_id, sender_type, message_content, metadata, timestamp
                        FROM chat_messages
                    """))
                    
                    # Drop old table and rename new table
                    conn.execute(text("DROP TABLE chat_messages"))
                    conn.execute(text("ALTER TABLE chat_messages_new RENAME TO chat_messages"))
                    
                elif db_dialect == 'mysql':
                    # MySQL syntax
                    conn.execute(text(
                        "ALTER TABLE chat_messages CHANGE metadata message_metadata JSON"
                    ))
                else:
                    print(f"⚠️  Unsupported database dialect: {db_dialect}")
                    print("Please manually rename the 'metadata' column to 'message_metadata' in the chat_messages table.")
                    return False
                
                # Commit the transaction
                trans.commit()
                print("✅ Migration completed successfully!")
                print("   Column 'metadata' has been renamed to 'message_metadata' in chat_messages table.")
                return True
                
            except Exception as e:
                # Rollback on error
                trans.rollback()
                raise e
                
    except SQLAlchemyError as e:
        print(f"❌ Database error during migration: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during migration: {e}")
        return False


def verify_migration():
    """
    Verify that the migration was successful
    """
    try:
        engine = create_engine(settings.DATABASE_URL)
        inspector = inspect(engine)
        
        if 'chat_messages' not in inspector.get_table_names():
            print("ℹ️  chat_messages table doesn't exist yet.")
            return True
            
        columns = [col['name'] for col in inspector.get_columns('chat_messages')]
        
        if 'message_metadata' in columns and 'metadata' not in columns:
            print("✅ Migration verification successful!")
            print("   The chat_messages table now has 'message_metadata' column instead of 'metadata'.")
            return True
        elif 'metadata' in columns:
            print("❌ Migration verification failed!")
            print("   The old 'metadata' column still exists.")
            return False
        else:
            print("ℹ️  No metadata-related columns found. This is normal for a fresh installation.")
            return True
            
    except Exception as e:
        print(f"❌ Error during verification: {e}")
        return False


if __name__ == "__main__":
    print("=== Chat Messages Metadata Column Migration ===")
    print()
    
    # Run migration
    success = migrate_metadata_column()
    
    if success:
        print()
        # Verify migration
        verify_migration()
    else:
        print("\n❌ Migration failed. Please check the errors above and try again.")
        sys.exit(1)
    
    print("\n=== Migration Complete ===")