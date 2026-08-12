import asyncio
import json
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel

# 1. DATABASE CONFIGURATION (SQLite / PostgreSQL)
DATABASE_URL = "sqlite:///./autospec_database.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- SQLALCHEMY DATABASE MODELS ---

class DBBrand(Base):
    __tablename__ = "brands"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True) # e.g. "BMW", "Škoda", "Audi"
    country = Column(String)
    models = relationship("DBModel", back_populates="brand_rel", cascade="all, delete")

class DBModel(Base):
    __tablename__ = "models"
    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"))
    name = Column(String, index=True) # e.g. "M3", "Superb", "RS6"
    brand_rel = relationship("DBBrand", back_populates="models")
    generations = relationship("DBGeneration", back_populates="model_rel", cascade="all, delete")

class DBGeneration(Base):
    __tablename__ = "generations"
    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("models.id"))
    code = Column(String, index=True) # e.g. "E46", "MK3", "C8"
    years = Column(String)
    engine_code = Column(String) # e.g. "S54B32", "2.0 TDI (CRMB)", "DJPB"
    stock_hp = Column(Integer)
    stock_nm = Column(Integer)
    gearbox_type = Column(String) # "Manual", "DSG", "DKG", "Automatic"
    rarity_score = Column(Float)
    tuning_stage1 = Column(JSON) # {"hp_gain": 40, "nm_gain": 80, "price_eur": 350}
    tuning_stage2 = Column(JSON)
    model_rel = relationship("DBModel", back_populates="generations")

Base.metadata.create_all(bind=engine)

# --- DB SEEDING FUNCTION (Automatické naplnenie dátami pri prvom spustení) ---

def seed_initial_database():
    db = SessionLocal()
    try:
        if db.query(DBBrand).first():
            return # Databáza už obsahuje dáta

        # Značka 1: BMW
        bmw = DBBrand(name="BMW", country="Nemecko")
        m3 = DBModel(name="M3", brand_rel=bmw)
        m3_e46 = DBGeneration(
            model_rel=m3, code="E46", years="2000-2006", engine_code="S54B32",
            stock_hp=343, stock_nm=365, gearbox_type="Manual 6-speed / SMG II",
            rarity_score=92.5,
            tuning_stage1={"hp_gain": 22, "nm_gain": 20, "price_eur": 550.0},
            tuning_stage2={"hp_gain": 45, "nm_gain": 40, "price_eur": 1800.0}
        )

        # Značka 2: Škoda
        skoda = DBBrand(name="Škoda", country="Česko")
        superb = DBModel(name="Superb", brand_rel=skoda)
        superb_mk3 = DBGeneration(
            model_rel=superb, code="MK3", years="2015-2023", engine_code="2.0 TDI (CRMB/DFHA)",
            stock_hp=150, stock_nm=340, gearbox_type="Manual 6-speed",
            rarity_score=45.0,
            tuning_stage1={"hp_gain": 40, "nm_gain": 80, "price_eur": 350.0},
            tuning_stage2={"hp_gain": 65, "nm_gain": 110, "price_eur": 1200.0}
        )

        # Značka 3: Audi
        audi = DBBrand(name="Audi", country="Nemecko")
        rs6 = DBModel(name="RS6", brand_rel=audi)
        rs6_c8 = DBGeneration(
            model_rel=rs6, code="C8", years="2019+", engine_code="DJPB 4.0 V8 TFSI",
            stock_hp=600, stock_nm=800, gearbox_type="Tiptronic 8-speed",
            rarity_score=95.0,
            tuning_stage1={"hp_gain": 100, "nm_gain": 150, "price_eur": 1200.0},
            tuning_stage2={"hp_gain": 180, "nm_gain": 220, "price_eur": 4500.0}
        )

        db.add_all([bmw, skoda, audi])
        db.commit()
        print("✅ Databáza úspešne naplnená základnými značkami a modelmi!")
    finally:
        db.close()

# Spustíme seedovanie pri štarte aplikácie
seed_initial_database()

# --- FASTAPI ENGINE ---

app = FastAPI(title="AutoSpec AI Engine with Seed Database", version="3.1.0")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ENDPOINTS FOR DATABASE & SCANNING ---

@app.get("/api/v3/brands")
def get_all_brands(db: Session = Depends(get_db)):
    """Vráti zoznam všetkých značiek a ich modelov v databáze"""
    brands = db.query(DBBrand).all()
    result = []
    for b in brands:
        result.append({
            "brand": b.name,
            "country": b.country,
            "models": [m.name for m in b.models]
        })
    return result

@app.get("/api/v3/specs/{brand_name}/{model_name}/{gen_code}")
def get_vehicle_specs(brand_name: str, model_name: str, gen_code: str, db: Session = Depends(get_db)):
    """Vyhľadá presné špecifikácie konkrétneho auta v databáze"""
    vehicle = db.query(DBGeneration).join(DBModel).join(DBBrand).\
        filter(DBBrand.name.ilike(brand_name)).\
        filter(DBModel.name.ilike(model_name)).\
        filter(DBGeneration.code.ilike(gen_code)).first()
    
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vozidlo nebolo nájdené v databáze.")

    return {
        "brand": vehicle.model_rel.brand_rel.name,
        "model": vehicle.model_rel.name,
        "generation": vehicle.code,
        "engine_code": vehicle.engine_code,
        "stock_hp": vehicle.stock_hp,
        "stock_nm": vehicle.stock_nm,
        "gearbox": vehicle.gearbox_type,
        "rarity_score": vehicle.rarity_score,
        "tuning_stage_1": vehicle.tuning_stage1,
        "tuning_stage_2": vehicle.tuning_stage2
    }

@app.post("/api/v3/scan")
async def scan_and_match_db(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Skenovanie fotky s automatickým párovaním na DB záznam"""
    # 1. Simulácia vision AI rozpoznania z fotky (napr. rozpoznané BMW M3 E46)
    detected_brand = "BMW"
    detected_model = "M3"
    detected_gen = "E46"

    # 2. Načítanie skutočných dát z databázy
    matched = db.query(DBGeneration).join(DBModel).join(DBBrand).\
        filter(DBBrand.name == detected_brand).\
        filter(DBModel.name == detected_model).\
        filter(DBGeneration.code == detected_gen).first()

    if not matched:
        return {"status": "recognized_but_not_in_db", "detected": f"{detected_brand} {detected_model} {detected_gen}"}

    return {
        "status": "success",
        "matched_from_db": True,
        "data": {
            "brand": matched.model_rel.brand_rel.name,
            "model": matched.model_rel.name,
            "generation": matched.code,
            "engine": matched.engine_code,
            "stock_hp": matched.stock_hp,
            "stock_nm": matched.stock_nm,
            "rarity_index": matched.rarity_score,
            "stage_1_tuning": matched.tuning_stage1
        }
    }
