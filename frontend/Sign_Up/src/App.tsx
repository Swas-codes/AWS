import './index.css';
import BackgroundVideo from './components/BackgroundVideo';
import AuthForm from './components/AuthForm';
import KineticCenterBuild from './components/smoothui/kinetic-center-build';

export default function App() {
  return (
    <div style={{ position: 'relative', width: '100%', height: '100%' }}>
      {/* Full-screen background video */}
      <BackgroundVideo />

      {/* LAUNCHLENS logo — fixed top-left corner */}
      <div className="brand-logo">
        <div className="brand-logo__icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M12 2L2 7l10 5 10-5-10-5z" />
            <path d="M2 17l10 5 10-5" />
            <path d="M2 12l10 5 10-5" />
          </svg>
        </div>
        <span className="brand-logo__text">LaunchLens</span>
      </div>

      {/* Main layout: form left, branding center-right */}
      <div className="page-container">
        {/* Auth form */}
        <AuthForm />

        {/* Branding & Headline */}
        <div className="branding-section">
          {/* Headline */}
          <h1 className="brand-headline">
            Know your customers<br />
            before you launch.
          </h1>

          {/* Kinetic animated text */}
          <div className="brand-kinetic">
            <KineticCenterBuild
              className="kinetic-left-align"
              phrases={[
                "Validate your idea",
                "Understand your audience",
                "Launch with confidence",
                "Grow from day one",
              ]}
              interval={2800}
            />
          </div>

          {/* Subtitle */}
          <p className="brand-subtitle">
            LaunchLens helps you discover who your customers really are,
            what they need, and how to reach them — all before you go live.
          </p>
        </div>
      </div>
    </div>
  );
}
