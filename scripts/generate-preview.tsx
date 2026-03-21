import React from 'react';
import { ImageResponse } from '@takumi-rs/image-response';
import { writeFileSync } from 'fs';

async function generatePreview() {
  const response = new ImageResponse(
    <div
      style={{
        width: '1200px',
        height: '630px',
        display: 'flex',
        flexDirection: 'column',
        backgroundColor: '#dc2626',
        fontFamily: 'system-ui, sans-serif',
        padding: '50px',
        position: 'relative',
      }}
    >
      {/* Flag pattern - white band */}
      <div
        style={{
          position: 'absolute',
          bottom: 0,
          left: 0,
          right: 0,
          height: '315px',
          backgroundColor: '#ffffff',
        }}
      />

      {/* Content overlay */}
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          position: 'relative',
          zIndex: 10,
          height: '100%',
        }}
      >
        {/* Header */}
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
            <div
              style={{
                display: 'flex',
                fontSize: '56px',
                fontWeight: 900,
                color: '#ffffff',
              }}
            >
              ID
            </div>
            <h1
              style={{
                fontSize: '52px',
                fontWeight: 800,
                color: '#ffffff',
                margin: 0,
              }}
            >
              Indonesia Government APIs
            </h1>
          </div>
          <p
            style={{
              fontSize: '24px',
              fontWeight: 500,
              color: '#fecaca',
              margin: '12px 0 0 0',
            }}
          >
            50+ data portals, APIs & data sources with Python examples
          </p>
        </div>

        {/* Status Cards */}
        <div
          style={{
            display: 'flex',
            gap: '20px',
            marginTop: '40px',
          }}
        >
          <div
            style={{
              display: 'flex',
              flexDirection: 'column',
              backgroundColor: '#ffffff',
              border: '4px solid #000000',
              borderRadius: '12px',
              padding: '20px 30px',
              boxShadow: '6px 6px 0px 0px #000000',
            }}
          >
            <span style={{ fontSize: '42px', fontWeight: 800, color: '#16a34a' }}>22</span>
            <span style={{ fontSize: '16px', fontWeight: 600, color: '#000000' }}>UP</span>
          </div>
          
          <div
            style={{
              display: 'flex',
              flexDirection: 'column',
              backgroundColor: '#ffffff',
              border: '4px solid #000000',
              borderRadius: '12px',
              padding: '20px 30px',
              boxShadow: '6px 6px 0px 0px #000000',
            }}
          >
            <span style={{ fontSize: '42px', fontWeight: 800, color: '#eab308' }}>6</span>
            <span style={{ fontSize: '16px', fontWeight: 600, color: '#000000' }}>GEO-BLOCKED</span>
          </div>
          
          <div
            style={{
              display: 'flex',
              flexDirection: 'column',
              backgroundColor: '#ffffff',
              border: '4px solid #000000',
              borderRadius: '12px',
              padding: '20px 30px',
              boxShadow: '6px 6px 0px 0px #000000',
            }}
          >
            <span style={{ fontSize: '42px', fontWeight: 800, color: '#f97316' }}>5</span>
            <span style={{ fontSize: '16px', fontWeight: 600, color: '#000000' }}>CF CHALLENGE</span>
          </div>
          
          <div
            style={{
              display: 'flex',
              flexDirection: 'column',
              backgroundColor: '#ffffff',
              border: '4px solid #000000',
              borderRadius: '12px',
              padding: '20px 30px',
              boxShadow: '6px 6px 0px 0px #000000',
            }}
          >
            <span style={{ fontSize: '42px', fontWeight: 800, color: '#dc2626' }}>17</span>
            <span style={{ fontSize: '16px', fontWeight: 600, color: '#000000' }}>DNS DEAD</span>
          </div>
        </div>

        {/* Features */}
        <div
          style={{
            display: 'flex',
            gap: '30px',
            marginTop: '35px',
          }}
        >
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
              backgroundColor: 'rgba(255,255,255,0.95)',
              padding: '12px 20px',
              borderRadius: '8px',
              border: '3px solid #000000',
            }}
          >
            <span style={{ fontSize: '18px', fontWeight: 700, color: '#000000' }}>Python Examples</span>
          </div>
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
              backgroundColor: 'rgba(255,255,255,0.95)',
              padding: '12px 20px',
              borderRadius: '8px',
              border: '3px solid #000000',
            }}
          >
            <span style={{ fontSize: '18px', fontWeight: 700, color: '#000000' }}>MCP Servers</span>
          </div>
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
              backgroundColor: 'rgba(255,255,255,0.95)',
              padding: '12px 20px',
              borderRadius: '8px',
              border: '3px solid #000000',
            }}
          >
            <span style={{ fontSize: '18px', fontWeight: 700, color: '#000000' }}>Agent Skill</span>
          </div>
        </div>

        {/* Footer */}
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginTop: 'auto',
          }}
        >
          <span style={{ fontSize: '20px', color: '#374151', fontWeight: 600 }}>
            github.com/suryast/indonesia-gov-apis
          </span>
          <div
            style={{
              display: 'flex',
              backgroundColor: '#dc2626',
              color: '#ffffff',
              padding: '12px 24px',
              borderRadius: '8px',
              fontWeight: 700,
              fontSize: '18px',
              border: '3px solid #000000',
            }}
          >
            status.datarakyat.id
          </div>
        </div>
      </div>
    </div>,
    {
      width: 1200,
      height: 630,
    }
  );

  const buffer = Buffer.from(await response.arrayBuffer());
  writeFileSync('public/og-preview.png', buffer);
  console.log('Generated public/og-preview.png');
}

generatePreview();
