"""Advanced professional visual asset management system for financial dashboard"""

import hashlib
from typing import Dict, List, Optional
from dataclasses import dataclass
import requests
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

@dataclass
class ImageAsset:
    """Represents a visual asset with multiple sources"""
    primary_url: str
    fallback_url: str
    alt_text: str
    category: str
    keywords: List[str]
    width: int = 1200
    height: int = 600

class FinancialAssetManager:
    """Professional financial dashboard visual asset management system"""
    
    # Financial-specific image categories with professional keywords
    FINANCIAL_CATEGORIES = {
        "hero": {
            "keywords": ["trading", "stock-market", "finance", "analytics", "business", "wall-street"],
            "description": "Hero banners for financial dashboard"
        },
        "charts": {
            "keywords": ["graphs", "analytics", "data", "statistics", "charts", "visualization"],
            "description": "Chart and data visualization imagery"
        },
        "portfolio": {
            "keywords": ["investment", "portfolio", "wealth", "growth", "success", "money"],
            "description": "Portfolio and investment imagery"
        },
        "market": {
            "keywords": ["wall-street", "trading-floor", "finance", "market", "economy", "nyse"],
            "description": "Market and trading floor imagery"
        },
        "technology": {
            "keywords": ["fintech", "technology", "digital", "innovation", "computers", "software"],
            "description": "Financial technology imagery"
        },
        "professional": {
            "keywords": ["business", "professional", "office", "corporate", "team", "meeting"],
            "description": "Professional business imagery"
        },
        "success": {
            "keywords": ["success", "achievement", "growth", "profit", "winning", "celebration"],
            "description": "Success and achievement imagery"
        }
    }
    
    def __init__(self):
        self.cache: Dict[str, ImageAsset] = {}
        self.cache_duration = timedelta(hours=24)  # Cache images for 24 hours
        self.last_cache_cleanup = datetime.now()
    
    def _cleanup_cache(self):
        """Remove expired cache entries"""
        if datetime.now() - self.last_cache_cleanup > timedelta(hours=1):
            current_time = datetime.now()
            expired_keys = [
                key for key, asset in self.cache.items()
                if hasattr(asset, 'cached_at') and 
                current_time - asset.cached_at > self.cache_duration
            ]
            
            for key in expired_keys:
                del self.cache[key]
            
            self.last_cache_cleanup = current_time
            logger.info(f"Cleaned up {len(expired_keys)} expired cache entries")
    
    def generate_image_key(self, category: str, index: int, width: int = 1200, height: int = 600) -> str:
        """Generate unique key for image caching"""
        key_string = f"financial_{category}_{index}_{width}x{height}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get_financial_images(
        self, 
        category: str = "hero", 
        count: int = 3,
        width: int = 1200,
        height: int = 600
    ) -> List[ImageAsset]:
        """Get contextually relevant financial images with caching"""
        
        self._cleanup_cache()
        
        if category not in self.FINANCIAL_CATEGORIES:
            logger.warning(f"Unknown category: {category}, using 'hero' as fallback")
            category = "hero"
        
        category_info = self.FINANCIAL_CATEGORIES[category]
        keywords = category_info["keywords"]
        images = []
        
        for i in range(count):
            cache_key = self.generate_image_key(category, i, width, height)
            
            # Check cache first
            if cache_key in self.cache:
                images.append(self.cache[cache_key])
                continue
            
            # Generate new image asset
            keyword = keywords[i % len(keywords)]
            seed = hash(f"financial_{category}_{i}") % 10000
            
            # Primary source: Unsplash with financial keywords
            primary_url = f"https://source.unsplash.com/{width}x{height}/?{keyword}&sig={seed}"
            
            # Fallback source: Lorem Picsum with seed
            fallback_url = f"https://picsum.photos/{width}/{height}?random={seed}"
            
            # Alternative fallback: Placeholder with financial theme
            placeholder_url = f"https://via.placeholder.com/{width}x{height}/1a1a2e/ffffff?text=Financial+Dashboard"
            
            asset = ImageAsset(
                primary_url=primary_url,
                fallback_url=fallback_url,
                alt_text=f"Professional {keyword} imagery for financial dashboard {category}",
                category=category,
                keywords=[keyword],
                width=width,
                height=height
            )
            
            # Add to cache with timestamp
            asset.cached_at = datetime.now()
            self.cache[cache_key] = asset
            images.append(asset)
        
        logger.info(f"Generated {len(images)} images for category: {category}")
        return images
    
    def get_hero_image(self, width: int = 1200, height: int = 400) -> ImageAsset:
        """Get a single hero image for the dashboard"""
        images = self.get_financial_images("hero", 1, width, height)
        return images[0] if images else self._get_fallback_image(width, height)
    
    def get_chart_background(self, width: int = 800, height: int = 400) -> ImageAsset:
        """Get background image for chart sections"""
        images = self.get_financial_images("charts", 1, width, height)
        return images[0] if images else self._get_fallback_image(width, height)
    
    def get_portfolio_images(self, count: int = 3) -> List[ImageAsset]:
        """Get images for portfolio section"""
        return self.get_financial_images("portfolio", count)
    
    def get_market_images(self, count: int = 4) -> List[ImageAsset]:
        """Get images for market overview section"""
        return self.get_financial_images("market", count)
    
    def _get_fallback_image(self, width: int, height: int) -> ImageAsset:
        """Get fallback image when all else fails"""
        return ImageAsset(
            primary_url=f"https://via.placeholder.com/{width}x{height}/1a1a2e/ffffff?text=Financial+Dashboard",
            fallback_url=f"https://via.placeholder.com/{width}x{height}/2c3e50/ecf0f1?text=Loading...",
            alt_text="Financial dashboard placeholder image",
            category="fallback",
            keywords=["placeholder"],
            width=width,
            height=height
        )
    
    def validate_image_url(self, url: str, timeout: int = 5) -> bool:
        """Validate if an image URL is accessible"""
        try:
            response = requests.head(url, timeout=timeout)
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"Image validation failed for {url}: {e}")
            return False
    
    def get_optimized_image_html(self, asset: ImageAsset, css_classes: str = "") -> str:
        """Generate optimized HTML for image with fallback handling"""
        return f'''
        <img 
            src="{asset.primary_url}" 
            alt="{asset.alt_text}"
            class="financial-image {css_classes}"
            loading="lazy"
            onerror="this.onerror=null; this.src='{asset.fallback_url}';"
            style="width: {asset.width}px; height: {asset.height}px; object-fit: cover;"
        />
        '''
    
    @staticmethod
    def generate_financial_css() -> str:
        """Generate CSS for professional financial dashboard images"""
        return """
        /* Professional Financial Dashboard Image System */
        .financial-image {
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
        }
        
        .financial-image:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        }
        
        .hero-financial {
            width: 100%;
            height: 400px;
            object-fit: cover;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        }
        
        .chart-background {
            width: 100%;
            height: 200px;
            object-fit: cover;
            border-radius: 8px;
            opacity: 0.1;
            position: absolute;
            top: 0;
            left: 0;
            z-index: -1;
        }
        
        .portfolio-image {
            width: 100%;
            height: 180px;
            object-fit: cover;
            border-radius: 8px;
            transition: transform 0.3s ease;
        }
        
        .portfolio-image:hover {
            transform: scale(1.05);
        }
        
        .market-thumbnail {
            width: 120px;
            height: 80px;
            object-fit: cover;
            border-radius: 6px;
            border: 2px solid rgba(255, 255, 255, 0.1);
        }
        
        .image-overlay {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(
                to bottom, 
                transparent 0%, 
                rgba(26, 26, 46, 0.8) 100%
            );
            border-radius: inherit;
            display: flex;
            align-items: flex-end;
            padding: 16px;
            color: white;
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        .financial-image:hover .image-overlay {
            opacity: 1;
        }
        
        .loading-placeholder {
            background: linear-gradient(90deg, #2c3e50 25%, #34495e 50%, #2c3e50 75%);
            background-size: 200% 100%;
            animation: loading 2s infinite;
        }
        
        @keyframes loading {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }
        
        @media (max-width: 768px) {
            .hero-financial {
                height: 250px;
            }
            
            .portfolio-image {
                height: 150px;
            }
            
            .market-thumbnail {
                width: 100px;
                height: 60px;
            }
        }
        
        /* Dark theme optimizations */
        .dark .financial-image {
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .dark .image-overlay {
            background: linear-gradient(
                to bottom, 
                transparent 0%, 
                rgba(0, 0, 0, 0.8) 100%
            );
        }
        """

# Global instance for easy access
financial_assets = FinancialAssetManager()

# Convenience functions
def get_dashboard_hero() -> ImageAsset:
    """Get hero image for dashboard"""
    return financial_assets.get_hero_image()

def get_chart_images(count: int = 3) -> List[ImageAsset]:
    """Get images for chart sections"""
    return financial_assets.get_financial_images("charts", count)

def get_portfolio_gallery(count: int = 4) -> List[ImageAsset]:
    """Get portfolio gallery images"""
    return financial_assets.get_portfolio_images(count)

def get_market_overview_images(count: int = 4) -> List[ImageAsset]:
    """Get market overview images"""
    return financial_assets.get_market_images(count)